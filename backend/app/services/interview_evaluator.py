import json
from typing import Dict, Any, List
from app.config import settings
from app.core.db import db
from app.models.interview import QuestionEvaluationResult, InterviewReport, StudyRecommendationItem

class InterviewEvaluator:
    """
    Evaluates student voice interview answers against technical dimensions,
    calculates deterministic final scores, and generates exact concept study recommendations.
    """
    
    DEFAULT_RUBRIC = {
        "technical_correctness": 0.40,
        "concept_understanding": 0.25,
        "reasoning": 0.15,
        "completeness": 0.10,
        "practical_understanding": 0.10
    }

    SYSTEM_PROMPT = """
You are an expert Computer Science interviewer evaluating a candidate's voice answer to a technical question.

CRITICAL RULES:
1. FOCUS EXCLUSIVELY ON TECHNICAL CONCEPTUAL UNDERSTANDING AND PRACTICAL REASONING.
2. DO NOT PENALIZE FOR NON-NATIVE ENGLISH GRAMMAR, ACCENT, PRONUNCIATION, OR MINOR SPEECH-TO-TEXT TYPOS.
3. Evaluate the student's answer across the 5 technical dimensions on a 0.0 to 1.0 scale:
   - technical_correctness (0.0 to 1.0)
   - concept_understanding (0.0 to 1.0)
   - reasoning (0.0 to 1.0)
   - completeness (0.0 to 1.0)
   - practical_understanding (0.0 to 1.0)
4. List any key missing technical concepts in `missing_concepts`.
5. Provide concise technical feedback.
6. DO NOT calculate the final weighted score — the backend engine will compute it deterministically.
"""

    @classmethod
    def evaluate_question_answer(cls, question_text: str, topic: str, student_answer: str) -> QuestionEvaluationResult:
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL, system_instruction=cls.SYSTEM_PROMPT)
                
                prompt = f"""
=== QUESTION ASKED ===
Topic: {topic}
Question: "{question_text}"

=== CANDIDATE VOICE TRANSCRIPT ANSWER ===
"{student_answer}"

=== TASK ===
Evaluate the technical answer and return JSON:
{{
  "technical_correctness": 0.85,
  "concept_understanding": 0.80,
  "reasoning": 0.75,
  "completeness": 0.70,
  "practical_understanding": 0.80,
  "missing_concepts": ["Specific optimization detail"],
  "technical_feedback": "Concise feedback explanation..."
}}
"""
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "temperature": 0.1})
                raw_json = response.text.strip()
                if raw_json.startswith("```json"):
                    raw_json = raw_json.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_json)
                
                # Calculate score deterministically
                raw_score = cls.calculate_question_score(data)
                return QuestionEvaluationResult(
                    question_id="",
                    technical_correctness=float(data.get("technical_correctness", 0.7)),
                    concept_understanding=float(data.get("concept_understanding", 0.7)),
                    reasoning=float(data.get("reasoning", 0.7)),
                    completeness=float(data.get("completeness", 0.7)),
                    practical_understanding=float(data.get("practical_understanding", 0.7)),
                    missing_concepts=data.get("missing_concepts", []),
                    technical_feedback=data.get("technical_feedback", "Solid technical explanation."),
                    question_score=raw_score
                )
            except Exception as e:
                print(f"[InterviewEvaluator] Gemini evaluation error: {e}. Using rule fallback.")

        # Fallback rule-based evaluator
        length = len(student_answer.split())
        base = min(1.0, length / 25.0)
        fallback_data = {
            "technical_correctness": round(min(1.0, base * 0.9 + 0.1), 2),
            "concept_understanding": round(min(1.0, base * 0.85 + 0.15), 2),
            "reasoning": round(min(1.0, base * 0.8), 2),
            "completeness": round(min(1.0, base * 0.75), 2),
            "practical_understanding": round(min(1.0, base * 0.8), 2)
        }
        score = cls.calculate_question_score(fallback_data)
        return QuestionEvaluationResult(
            question_id="",
            technical_correctness=fallback_data["technical_correctness"],
            concept_understanding=fallback_data["concept_understanding"],
            reasoning=fallback_data["reasoning"],
            completeness=fallback_data["completeness"],
            practical_understanding=fallback_data["practical_understanding"],
            missing_concepts=["Provide explicit complexity justifications"] if score < 70 else [],
            technical_feedback="Solid technical response. Explain trade-offs and edge cases explicitly.",
            question_score=score
        )

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
        """
        PART 18: Generates exact concept recommendations from actual topic weaknesses.
        """
        CONCEPT_MAP = {
            "DBMS": ["B-Tree Indexes", "Hash Indexes", "Clustered vs Non-Clustered Indexes", "Query Execution Plans", "Index Selectivity"],
            "Indexing": ["B-Tree Indexes", "Hash Indexes", "Composite Indexes", "Index Scan vs Table Scan"],
            "RAG": ["BM25 Sparse Retrieval", "Dense Vector Embeddings", "Sparse vs Dense Retrieval", "Reciprocal Rank Fusion", "Reranking Architectures"],
            "Hybrid Search": ["BM25 Sparse Retrieval", "Vector Search", "Reciprocal Rank Fusion", "Reranker Models"],
            "FastAPI": ["Async / Await Event Loop", "Pydantic Schemas", "Dependency Injection", "Uvicorn Workers"],
            "PostgreSQL": ["ACID Isolation Levels", "MVCC Concurrency", "EXPLAIN ANALYZE", "Partitioning"],
            "System Design": ["Load Balancing", "Horizontal Scaling", "Database Sharding", "Caching Strategies"],
            "Python": ["GIL (Global Interpreter Lock)", "Generators & Iterators", "Decorator Wrappers", "Memory Management"]
        }

        recommendations = []
        for topic, score in topic_scores.items():
            if score < 70.0:
                concepts = CONCEPT_MAP.get(topic, [
                    f"Core {topic} Architecture",
                    f"{topic} Performance Bottlenecks",
                    f"{topic} Best Practices",
                    f"{topic} Edge Case Handling",
                    f"{topic} Production Trade-offs"
                ])
                recommendations.append(StudyRecommendationItem(
                    topic=topic,
                    score=score,
                    exact_concepts=concepts
                ))
        return recommendations
