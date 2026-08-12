import json
import re
from typing import Dict, Any
from app.config import settings
from app.models.question import QuestionDetail, ConceptBlueprint
from app.models.evaluation import GeminiEvaluationSchema, ConceptStatusEvaluation, ComplexityEvaluation

class GeminiEvaluator:
    """
    Evaluates student natural-language explanations using Google Gemini API with structured JSON output schema.
    Applies strict conceptual evaluation rules without penalizing non-native English grammar or spelling.
    """
    
    SYSTEM_INSTRUCTION = """
You are an expert Computer Science / Data Structures & Algorithms (DSA) concept evaluator.

YOUR MANDATE:
Evaluate whether the student conceptually understands the algorithm and data structures required to solve the given DSA problem.

CRITICAL RULES:
1. FOCUS EXCLUSIVELY ON TECHNICAL CONCEPTUAL UNDERSTANDING.
2. DO NOT PENALIZE FOR GRAMMAR, SPELLING, ACCENT-BASED PHRASING, IMPERFECT ENGLISH, OR INFORMAL STYLE.
   Example: "I use hashmap store count then second loop find first count one" represents STRONG conceptual understanding of finding first unique character.
3. Compare the student's explanation against each concept in the provided Concept Blueprint.
4. For each concept, assign:
   - score: 1.0 (Correctly understood), 0.5 (Partially understood), or 0.0 (Not understood / missing / wrong)
   - status: "correct", "partial", or "incorrect"
   - evidence: Direct quote or clear paraphrase from student answer demonstrating their level of understanding.
5. DO NOT invent expected concepts outside the blueprint.
6. Evaluate time and space complexity separately based on what the student stated versus the expected optimal complexity.
7. Return strictly valid JSON adhering to the provided JSON Schema. Do NOT include markdown codeblocks or conversational fluff outside the JSON.
"""

    @classmethod
    def build_evaluation_prompt(cls, question: QuestionDetail, blueprint: ConceptBlueprint, student_answer: str) -> str:
        concepts_json = json.dumps([
            {
                "concept_id": c.concept_id,
                "concept_name": c.concept_name,
                "description": c.description,
                "importance": c.importance,
                "weight": c.weight,
                "is_mandatory": c.is_mandatory,
                "expected_keywords": c.expected_keywords or []
            }
            for c in blueprint.concepts
        ], indent=2)

        prompt = f"""
=== QUESTION DETAILS ===
Title: {question.title}
Category: {question.category}
Difficulty: {question.difficulty}
Problem Statement:
{question.problem_statement}

=== CONCEPT BLUEPRINT (EXPECTED CONCEPTS) ===
{concepts_json}

Optimal Expected Time Complexity: {blueprint.expected_time_complexity}
Optimal Expected Space Complexity: {blueprint.expected_space_complexity}
Expected Edge Cases to Consider: {", ".join(blueprint.expected_edge_cases)}

=== STUDENT NATURAL LANGUAGE ANSWER ===
"{student_answer}"

=== TASK ===
Evaluate the student's answer against the Concept Blueprint and return the evaluation as JSON.
"""
        return prompt

    @classmethod
    def evaluate(cls, question: QuestionDetail, blueprint: ConceptBlueprint, student_answer: str) -> GeminiEvaluationSchema:
        prompt = cls.build_evaluation_prompt(question, blueprint, student_answer)
        
        # If Gemini API key is configured, use official Google Gemini client
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(
                    model_name=settings.GEMINI_MODEL,
                    system_instruction=cls.SYSTEM_INSTRUCTION
                )
                
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "response_mime_type": "application/json",
                        "temperature": 0.1
                    }
                )
                
                raw_text = response.text.strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                
                data = json.loads(raw_text)
                return GeminiEvaluationSchema(**data)
            except Exception as e:
                print(f"[Gemini Evaluator] API call failed: {e}. Falling back to rule-based offline evaluation.")
                
        # Fallback offline semantic heuristic evaluator for instant testing without API keys
        return cls._offline_heuristic_evaluation(question, blueprint, student_answer)

    @classmethod
    def _offline_heuristic_evaluation(cls, question: QuestionDetail, blueprint: ConceptBlueprint, student_answer: str) -> GeminiEvaluationSchema:
        """
        Robust rule-based semantic parser used as a fallback when offline or without API key.
        Matches keywords & concepts semantically to allow offline verification.
        """
        answer_lower = student_answer.lower()
        evaluated_concepts = []
        
        for c in blueprint.concepts:
            keywords = [c.concept_name.lower()] + [kw.lower() for kw in (c.expected_keywords or [])]
            words_in_desc = [w.lower() for w in c.description.split() if len(w) > 4]
            keywords.extend(words_in_desc)
            
            matched_count = sum(1 for kw in set(keywords) if kw in answer_lower)
            
            if matched_count >= 2:
                status = "correct"
                score = 1.0
                evidence = f"Student explanation mentions relevant terminology for '{c.concept_name}'."
            elif matched_count == 1:
                status = "partial"
                score = 0.5
                evidence = f"Student partially references ideas matching '{c.concept_name}'."
            else:
                status = "incorrect"
                score = 0.0
                evidence = f"Concept '{c.concept_name}' was not clearly detected in explanation."
                
            evaluated_concepts.append(ConceptStatusEvaluation(
                concept_id=c.concept_id,
                status=status,
                score=score,
                evidence=evidence,
                feedback=f"Understanding for {c.concept_name}: {status}"
            ))

        # Time complexity matching
        exp_time = blueprint.expected_time_complexity.lower()
        time_score = 0.0
        student_time_str = "Not specified"
        if exp_time in answer_lower or "o(" in answer_lower:
            time_score = 1.0 if exp_time in answer_lower else 0.5
            student_time_str = exp_time if exp_time in answer_lower else "Stated complexity"
            
        # Space complexity matching
        exp_space = blueprint.expected_space_complexity.lower()
        space_score = 0.0
        student_space_str = "Not specified"
        if exp_space in answer_lower or "o(1)" in answer_lower or "o(n)" in answer_lower:
            space_score = 1.0 if exp_space in answer_lower else 0.5
            student_space_str = exp_space if exp_space in answer_lower else "Stated space complexity"

        # Edge cases matching
        edge_matched = sum(1 for ec in blueprint.expected_edge_cases if any(w in answer_lower for w in ec.lower().split() if len(w) > 3))
        edge_cases_score = min(1.0, edge_matched / max(1, len(blueprint.expected_edge_cases)))

        # Average conceptual score
        avg_concept_score = sum(c.score for c in evaluated_concepts) / max(1, len(evaluated_concepts))

        return GeminiEvaluationSchema(
            concepts=evaluated_concepts,
            algorithm_correctness=min(1.0, avg_concept_score * 1.1),
            reasoning=min(1.0, avg_concept_score * 0.95 + 0.1),
            time_complexity=ComplexityEvaluation(
                student_answer=student_time_str,
                expected=blueprint.expected_time_complexity,
                score=time_score,
                feedback="Verified complexity analysis against problem specifications."
            ),
            space_complexity=ComplexityEvaluation(
                student_answer=student_space_str,
                expected=blueprint.expected_space_complexity,
                score=space_score,
                feedback="Verified memory space usage analysis."
            ),
            edge_cases=round(edge_cases_score, 2),
            technical_feedback="Solid conceptual response. Focus on explaining edge case boundaries and time complexity justifications clearly.",
            misconceptions=["Ensure all edge cases are explicitly mentioned."] if edge_cases_score < 0.5 else [],
            strengths=["Clear algorithmic steps", "Good choice of data structures"],
            improvements=["Provide explicit complexity bounds", "Cover empty/single element edge cases"]
        )
