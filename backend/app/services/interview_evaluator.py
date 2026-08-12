import json
from typing import Dict, Any, List
from app.config import settings
from app.core.db import db
from app.models.interview import QuestionEvaluationResult, StudyRecommendationItem

class InterviewEvaluator:
    """
    Evaluates student technical answers with explicit support for:
    - English, Hindi, and Hinglish spoken answers.
    - Zero penalty for non-native English grammar, accents, or language mixing.
    - Low speech confidence detection (re-prompting without penalizing technical score).
    """

    DEFAULT_RUBRIC = {
        "technical_correctness": 0.40,
        "concept_understanding": 0.25,
        "reasoning": 0.15,
        "completeness": 0.10,
        "practical_understanding": 0.10
    }

    SYSTEM_PROMPT = """
You are an expert Computer Science interviewer evaluating a candidate's spoken voice answer.

CRITICAL FAIRNESS & HINGLISH RULES:
1. THE CANDIDATE MAY ANSWER IN ENGLISH, HINDI, OR HINGLISH (e.g. "Hum pehle vector embedding generate karte hain then Qdrant mein store karte hain").
2. INTERPRET THE TECHNICAL MEANING, CONCEPTUAL UNDERSTANDING, AND REASONING ACCURATELY REGARDLESS OF HINDI/HINGLISH GRAMMAR OR MIXING.
3. DO NOT PENALIZE FOR NON-NATIVE ACCENTS, SPEECH-TO-TEXT TYPOS, OR HINGLISH PHRASING.
4. If the speech transcript is completely unintelligible or noise ("asdfgh", "unclear audio"), set `"low_speech_confidence": true`.
5. Evaluate across 5 dimensions on a 0.0 to 1.0 scale:
   - technical_correctness (0.0 to 1.0)
   - concept_understanding (0.0 to 1.0)
   - reasoning (0.0 to 1.0)
   - completeness (0.0 to 1.0)
   - practical_understanding (0.0 to 1.0)
6. List missing technical concepts in `missing_concepts`.
7. Provide concise technical feedback in English.
"""

    @classmethod
    def evaluate_question_answer(cls, question_text: str, topic: str, student_answer: str) -> Dict[str, Any]:
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL, system_instruction=cls.SYSTEM_PROMPT)

                prompt = f"""
=== QUESTION ASKED ===
Topic: {topic}
Question: "{question_text}"

=== CANDIDATE SPOKEN ANSWER (English / Hinglish / Hindi) ===
"{student_answer}"

=== TASK ===
Evaluate technical conceptual understanding and return JSON:
{{
  "technical_correctness": 0.85,
  "concept_understanding": 0.80,
  "reasoning": 0.75,
  "completeness": 0.70,
  "practical_understanding": 0.80,
  "low_speech_confidence": false,
  "missing_concepts": ["BM25"],
  "technical_feedback": "Concise technical feedback..."
}}
"""
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "temperature": 0.1})
                raw_json = response.text.strip()
                if raw_json.startswith("```json"):
                    raw_json = raw_json.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_json)

                if data.get("low_speech_confidence", False):
                    return {
                        "low_speech_confidence": True,
                        "feedback": "Sorry, I couldn't catch that clearly. Could you repeat your answer?"
                    }

                score = cls.calculate_question_score(data)
                return {
                    "low_speech_confidence": False,
                    "technical_correctness": float(data.get("technical_correctness", 0.7)),
                    "concept_understanding": float(data.get("concept_understanding", 0.7)),
                    "reasoning": float(data.get("reasoning", 0.7)),
                    "completeness": float(data.get("completeness", 0.7)),
                    "practical_understanding": float(data.get("practical_understanding", 0.7)),
                    "missing_concepts": data.get("missing_concepts", []),
                    "technical_feedback": data.get("technical_feedback", "Solid technical explanation."),
                    "question_score": score
                }
            except Exception as e:
                print(f"[InterviewEvaluator] Gemini evaluation error: {e}. Using fallback.")

        # Fallback rule evaluator
        words = student_answer.split()
        if len(words) < 2:
            return {
                "low_speech_confidence": True,
                "feedback": "Sorry, I couldn't catch that clearly. Could you repeat your answer?"
            }

        length = len(words)
        base = min(1.0, length / 20.0)
        fallback_data = {
            "technical_correctness": round(min(1.0, base * 0.9 + 0.1), 2),
            "concept_understanding": round(min(1.0, base * 0.85 + 0.15), 2),
            "reasoning": round(min(1.0, base * 0.8), 2),
            "completeness": round(min(1.0, base * 0.75), 2),
            "practical_understanding": round(min(1.0, base * 0.8), 2)
        }
        score = cls.calculate_question_score(fallback_data)
        return {
            "low_speech_confidence": False,
            "technical_correctness": fallback_data["technical_correctness"],
            "concept_understanding": fallback_data["concept_understanding"],
            "reasoning": fallback_data["reasoning"],
            "completeness": fallback_data["completeness"],
            "practical_understanding": fallback_data["practical_understanding"],
            "missing_concepts": ["Provide detailed trade-off analysis"] if score < 70 else [],
            "technical_feedback": "Good technical understanding shown.",
            "question_score": score
        }

    @classmethod
    def calculate_question_score(cls, dims: Dict[str, float]) -> float:
        w = cls.DEFAULT_RUBRIC
        score_0_1 = (
            (dims.get("technical_correctness", 0.7) * w["technical_correctness"]) +
            (dims.get("concept_understanding", 0.7) * w["concept_understanding"]) +
            (dims.get("reasoning", 0.7) * w["reasoning"]) +
            (dims.get("completeness", 0.7) * w["completeness"]) +
            (dims.get("practical_understanding", 0.7) * w["practical_understanding"])
        )
        return round(min(max(score_0_1 * 100.0, 0.0), 100.0), 1)

    @classmethod
    def generate_exact_study_recommendations(cls, topic_scores: Dict[str, float]) -> List[StudyRecommendationItem]:
        CONCEPT_MAP = {
            "DBMS & SQL": ["B-Tree Indexes", "Hash Indexes", "ACID Isolation Levels", "EXPLAIN ANALYZE Query Plans", "Index Selectivity"],
            "Project Architecture": ["Microservices vs Monolith", "Async Event Loops", "Caching Strategies", "Load Balancing", "Failure Recovery"],
            "Data Structures & Algorithms": ["Time vs Space Complexity", "Dynamic Programming Trade-offs", "Graph Traversals", "Hash Map Collisions"],
            "Operating Systems & Concurrency": ["Process vs Thread", "Mutex Locks & Deadlocks", "Virtual Memory & Paging", "Context Switching Overhead"],
            "Computer Networks": ["TCP 3-Way Handshake", "HTTP/2 vs HTTP/3", "DNS Resolution", "REST vs gRPC"],
            "RAG": ["BM25 Sparse Retrieval", "Dense Vector Embeddings", "Reciprocal Rank Fusion", "Reranking Architectures", "Context Window Limits"]
        }

        recommendations = []
        for topic, score in topic_scores.items():
            if score < 70.0:
                concepts = CONCEPT_MAP.get(topic, [
                    f"Core {topic} Architecture",
                    f"{topic} Performance Tuning",
                    f"{topic} Production Best Practices",
                    f"{topic} Edge Case Handling",
                    f"{topic} Architectural Trade-offs"
                ])
                recommendations.append(StudyRecommendationItem(
                    topic=topic,
                    score=score,
                    exact_concepts=concepts
                ))
        return recommendations
