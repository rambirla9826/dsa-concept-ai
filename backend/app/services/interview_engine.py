import json
import re
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.config import settings
from app.core.db import db
from app.models.interview import QuestionGenerated

class InterviewEngine:
    """
    Upgraded Real-time Human-like Interview Engine:
    - Placement topic weighting matrix
    - Semantic deduplication engine
    - Hinglish / Hindi technical term parser
    - Phonetic tech term corrector
    - Short conversational reaction generator
    - Adaptive real-time follow-up generator
    """

    # Software Engineering Placement Weighting Matrix
    TOPIC_WEIGHTS = {
        "Project Architecture": 0.25,
        "Data Structures & Algorithms": 0.20,
        "DBMS & SQL": 0.10,
        "Operating Systems & Concurrency": 0.10,
        "Object Oriented Programming & Design": 0.10,
        "Programming Fundamentals": 0.10,
        "System & Role Knowledge": 0.10,
        "Computer Networks": 0.05
    }

    QUESTION_STYLES = [
        "Scenario", "Why", "How", "Debugging",
        "Architecture", "Trade-off", "Comparison", "Practical"
    ]

    # Technical phonetic term corrections map
    PHONETIC_CORRECTIONS = {
        "q drain": "Qdrant",
        "q-drain": "Qdrant",
        "q drent": "Qdrant",
        "fast api": "FastAPI",
        "fast-api": "FastAPI",
        "post gress": "PostgreSQL",
        "post-gress": "PostgreSQL",
        "b m 25": "BM25",
        "bm 25": "BM25",
        "r a g": "RAG",
        "rag": "RAG",
        "lang chain": "LangChain",
        "vector DB": "Vector Database"
    }

    @classmethod
    def correct_phonetic_terms(cls, text: str, resume_topics: List[str]) -> str:
        """
        Contextually corrects common Speech-to-Text misinterpretations based on candidate's resume.
        """
        corrected = text
        for term, replacement in cls.PHONETIC_CORRECTIONS.items():
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            corrected = pattern.sub(replacement, corrected)
            
        for topic in resume_topics:
            if topic and len(topic) > 3:
                # If term in text is very close phonetically, ensure topic casing
                pattern = re.compile(re.escape(topic), re.IGNORECASE)
                corrected = pattern.sub(topic, corrected)
                
        return corrected

    @classmethod
    def check_and_reserve_attempt(cls, user_id: str) -> Dict[str, Any]:
        limit_doc = db.get_document("interview_limits", user_id)
        if not limit_doc:
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
            raise ValueError("AI Technical Interview access has been disabled by administrator.")

        allowed = limit_doc.get("allowed_interviews", 5)
        used = limit_doc.get("used_interviews", 0)
        is_unlimited = limit_doc.get("is_unlimited", False)

        if not is_unlimited and used >= allowed:
            raise ValueError(f"You have used all available interview attempts ({used}/{allowed}). Contact administrator for extra attempts.")

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
        all_iqs = db.query_collection("interview_questions", "user_id", user_id)
        return [q.get("question_text", "") for q in all_iqs if q.get("question_text")]

    @classmethod
    def is_duplicate_question(cls, candidate_q: str, past_questions: List[str], threshold: float = 0.65) -> bool:
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
    def generate_short_reaction_and_question(
        cls,
        user_id: str,
        interview_id: str,
        resume_doc: Dict[str, Any],
        current_q_num: int,
        last_answer: Optional[str] = None,
        last_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generates a 1-sentence natural bridge reaction + a fresh real-world technical question or adaptive follow-up.
        """
        past_questions = cls.get_past_user_questions(user_id)
        extracted_skills = resume_doc.get("skills", ["Python", "FastAPI", "PostgreSQL", "RAG"])
        compact_context = resume_doc.get("compact_context", "Candidate with software engineering skills.")
        projects = resume_doc.get("projects", [])

        # Select topic based on placement weighting & question number
        if projects and current_q_num == 1:
            target_topic = projects[0].get("name", "Project Architecture")
            style = "Architecture"
        elif current_q_num == 2:
            target_topic = extracted_skills[0] if extracted_skills else "Data Structures"
            style = "Scenario"
        elif current_q_num == 3:
            target_topic = "DBMS & SQL"
            style = "Trade-off"
        elif current_q_num == 4:
            target_topic = "Operating Systems & Concurrency"
            style = "Debugging"
        else:
            target_topic = extracted_skills[1] if len(extracted_skills) > 1 else "System Design"
            style = "Practical"

        # Adaptive follow-up flag if candidate gave previous answer
        is_followup = bool(last_answer and len(last_answer.split()) >= 3)

        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL)

                if is_followup:
                    prompt = f"""
You are a senior professional Indian female technical interviewer conducting a live software engineering placement interview.
Candidate Resume Context: "{compact_context}"
Candidate Last Spoken Answer (May be in English, Hindi, or Hinglish): "{last_answer}"
Target Topic: "{target_topic}"

TASK:
1. Generate a brief 1-sentence natural conversational reaction in English (e.g., "Got it, that makes sense.", "Okay, right.", "Interesting approach.")
2. Generate an ADAPTIVE FOLLOW-UP question (1-2 sentences in English) derived directly from the candidate's last answer. If score was high, ask a deeper scenario/trade-off. If low, ask a foundational query.
3. Past Questions Asked (DO NOT REPEAT): {json.dumps(past_questions)}

Return JSON:
{{
  "reaction": "Brief 1-sentence reaction",
  "question_text": "Single clear 1-2 sentence spoken question in English",
  "topic": "{target_topic}",
  "difficulty": "Medium",
  "question_type": "Adaptive Follow-up"
}}
"""
                else:
                    prompt = f"""
You are a senior professional Indian female technical interviewer conducting a live software engineering placement interview.
Candidate Resume Context: "{compact_context}"
Target Topic: "{target_topic}"
Question Style: "{style}"
Question Number: {current_q_num} of 5.
Past Questions Asked (DO NOT REPEAT): {json.dumps(past_questions)}

Generate a single clear, natural technical interview question (1-2 sentences in English) suitable for live spoken interview.
Return JSON:
{{
  "reaction": "Hi! Let's get started with your technical assessment." if current_q_num == 1 else "Okay, let's move to the next area.",
  "question_text": "Single clear 1-2 sentence spoken question in English",
  "topic": "{target_topic}",
  "difficulty": "Medium",
  "question_type": "{style}"
}}
"""

                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "temperature": 0.2})
                raw_json = response.text.strip()
                if raw_json.startswith("```json"):
                    raw_json = raw_json.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_json)
                q_text = data.get("question_text", "")

                if not cls.is_duplicate_question(q_text, past_questions):
                    return {
                        "question_id": f"iq_{uuid.uuid4().hex[:10]}",
                        "question_number": current_q_num,
                        "reaction": data.get("reaction", "Got it."),
                        "question_text": q_text,
                        "topic": data.get("topic", target_topic),
                        "difficulty": data.get("difficulty", "Medium"),
                        "question_type": data.get("question_type", style)
                    }
            except Exception as e:
                print(f"[InterviewEngine] Gemini adaptive question error: {e}. Using rule fallback.")

        # Fallback question generator
        fallback_questions = [
            f"Walk me through how you designed {target_topic} in your project and the key architectural trade-offs you considered.",
            f"Suppose a service using {target_topic} experiences sudden high query latency in production. How would you debug it?",
            f"When would you choose a different data structure or approach over {target_topic}?",
            f"How do concurrency and lock contention affect performance when scaling {target_topic}?",
            f"Explain how failure recovery and data integrity are handled in {target_topic}."
        ]

        q_text = fallback_questions[0]
        for fq in fallback_questions:
            if not cls.is_duplicate_question(fq, past_questions):
                q_text = fq
                break

        return {
            "question_id": f"iq_{uuid.uuid4().hex[:10]}",
            "question_number": current_q_num,
            "reaction": "Got it. Let's look at this next.",
            "question_text": q_text,
            "topic": target_topic,
            "difficulty": "Medium",
            "question_type": style
        }
