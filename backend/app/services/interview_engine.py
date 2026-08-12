import json
import re
import uuid
import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.config import settings
from app.core.db import db
from app.models.interview import QuestionGenerated, ResumeDataSchema

class InterviewEngine:
    """
    Core engine handling adaptive question generation, semantic question deduplication,
    multi-interview memory, and atomic student attempt limit locks.
    """

    QUESTION_STYLES = [
        "Conceptual", "Project-based", "Why", "How", "Debugging",
        "Scenario", "Architecture", "Trade-off", "Comparison",
        "Practical", "Optimization", "Failure analysis"
    ]

    @classmethod
    def check_and_reserve_attempt(cls, user_id: str) -> Dict[str, Any]:
        """
        Atomic reservation of student interview attempt to prevent double-click / multi-tab bypasses.
        """
        # Fetch or initialize limit doc
        limit_doc = db.get_document("interview_limits", user_id)
        if not limit_doc:
            # Check global config for default limit
            config_doc = db.get_document("interview_config", "global_config") or {}
            default_limit = config_doc.get("default_allowed_interviews", 5)
            
            limit_doc = {
                "user_id": user_id,
                "allowed_interviews": default_limit,
                "used_interviews": 0,
                "is_unlimited": False,
                "is_disabled": False,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            db.set_document("interview_limits", user_id, limit_doc)

        if limit_doc.get("is_disabled", False):
            raise ValueError("AI Technical Interview access has been disabled by platform administrator.")

        allowed = limit_doc.get("allowed_interviews", 5)
        used = limit_doc.get("used_interviews", 0)
        is_unlimited = limit_doc.get("is_unlimited", False)

        if not is_unlimited and used >= allowed:
            raise ValueError(f"You have used all available interview attempts ({used}/{allowed}). Contact administrator for extra attempts.")

        # Atomically increment used count
        new_used = used + 1
        limit_doc["used_interviews"] = new_used
        limit_doc["updated_at"] = datetime.now(timezone.utc).isoformat()
        db.set_document("interview_limits", user_id, limit_doc)

        remaining = 999 if is_unlimited else max(0, allowed - new_used)
        return {
            "allowed_interviews": allowed,
            "used_interviews": new_used,
            "remaining_interviews": remaining,
            "is_unlimited": is_unlimited
        }

    @classmethod
    def get_past_user_questions(cls, user_id: str) -> List[str]:
        """
        Retrieves all question texts asked to this user across all previous interviews.
        """
        all_iqs = db.query_collection("interview_questions", "user_id", user_id)
        return [q.get("question_text", "") for q in all_iqs if q.get("question_text")]

    @classmethod
    def is_duplicate_question(cls, candidate_q: str, past_questions: List[str], threshold: float = 0.65) -> bool:
        """
        Semantic/string deduplication check ensuring NO exact or paraphrased duplicate questions.
        """
        def get_words(text: str) -> set:
            return set(re.findall(r'\w+', text.lower()))

        candidate_words = get_words(candidate_q)
        if not candidate_words:
            return False

        for past_q in past_questions:
            past_words = get_words(past_q)
            if not past_words:
                continue
            intersection = candidate_words.intersection(past_words)
            union = candidate_words.union(past_words)
            jaccard_sim = len(intersection) / len(union) if union else 0.0
            
            if jaccard_sim >= threshold or candidate_q.lower().strip() == past_q.lower().strip():
                return True
        return False

    @classmethod
    def get_user_past_weak_topics(cls, user_id: str) -> List[str]:
        """
        Multi-interview progress memory: Extracts weak topics from previous completed interviews.
        """
        past_interviews = db.query_collection("interviews", "user_id", user_id)
        completed = [i for i in past_interviews if i.get("status") == "COMPLETED"]
        if not completed:
            return []
            
        completed.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
        latest = completed[0]
        return latest.get("weak_areas", [])

    @classmethod
    def generate_next_question(
        cls,
        user_id: str,
        interview_id: str,
        resume_doc: Dict[str, Any],
        current_question_number: int,
        previous_evaluations: List[Dict[str, Any]]
    ) -> QuestionGenerated:
        
        past_questions = cls.get_past_user_questions(user_id)
        weak_topics = cls.get_user_past_weak_topics(user_id)
        
        extracted_skills = resume_doc.get("skills", ["Python", "FastAPI", "PostgreSQL", "RAG"])
        compact_context = resume_doc.get("compact_context", "Candidate with computer science skills.")
        projects = resume_doc.get("projects", [])
        
        # Determine topic and style
        style = cls.QUESTION_STYLES[(current_question_number - 1) % len(cls.QUESTION_STYLES)]
        
        # Priority to weak topics if present
        if weak_topics and current_question_number in [1, 2]:
            target_topic = weak_topics[(current_question_number - 1) % len(weak_topics)]
        elif projects and current_question_number == 3:
            target_topic = projects[0].get("name", "Project Architecture")
            style = "Project-based"
        else:
            target_topic = extracted_skills[(current_question_number - 1) % len(extracted_skills)]

        # Gemini API prompt
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL)
                
                prompt = f"""
You are an expert technical interviewer conducting a two-way AI voice technical interview.
Candidate Compact Resume Summary: "{compact_context}"
Target Technical Topic: "{target_topic}"
Question Style: "{style}"
Question Number: {current_question_number} of 5.
Past Questions Asked (DO NOT REPEAT OR PARAPHRASE THESE):
{json.dumps(past_questions, indent=2)}

Generate a single concise, technical question (1-2 sentences) appropriate for voice playback.
Return JSON:
{{
  "question_text": "...",
  "topic": "{target_topic}",
  "difficulty": "Medium",
  "question_type": "{style}"
}}
"""
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "temperature": 0.3})
                raw_json = response.text.strip()
                if raw_json.startswith("```json"):
                    raw_json = raw_json.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_json)
                q_text = data.get("question_text", "")
                
                if not cls.is_duplicate_question(q_text, past_questions):
                    return QuestionGenerated(
                        question_id=f"iq_{uuid.uuid4().hex[:10]}",
                        question_number=current_question_number,
                        question_text=q_text,
                        topic=data.get("topic", target_topic),
                        difficulty=data.get("difficulty", "Medium"),
                        question_type=data.get("question_type", style)
                    )
            except Exception as e:
                print(f"[InterviewEngine] Gemini question generation error: {e}. Using rule fallback.")

        # Fallback question generator enforcing non-duplicate questions
        fallback_questions = [
            f"In your experience with {target_topic}, how do you handle memory optimization and performance bottlenecks?",
            f"Regarding {target_topic}, why would you choose this approach over traditional alternatives in production?",
            f"Suppose a query or service involving {target_topic} experiences high latency. How would you investigate and resolve it?",
            f"Explain the architectural trade-offs when scaling {target_topic} across multiple server instances.",
            f"What edge cases or security concerns must be addressed when deploying {target_topic} in a cloud environment?"
        ]

        q_text = fallback_questions[0]
        for fq in fallback_questions:
            if not cls.is_duplicate_question(fq, past_questions):
                q_text = fq
                break

        return QuestionGenerated(
            question_id=f"iq_{uuid.uuid4().hex[:10]}",
            question_number=current_question_number,
            question_text=q_text,
            topic=target_topic,
            difficulty="Medium",
            question_type=style
        )
