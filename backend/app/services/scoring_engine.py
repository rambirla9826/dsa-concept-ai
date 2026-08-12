from typing import Dict, Any, List
from app.models.evaluation import GeminiEvaluationSchema, ConceptStatusEvaluation
from app.models.question import ConceptBlueprint

class ScoringEngine:
    """
    Deterministic scoring engine that takes structured concept-level evaluations
    and calculates the standardized final score on a 0-100 scale using configurable rubric weights.
    
    The LLM NEVER generates the final numerical score. This engine guarantees 100%
    deterministic, reproducible results for auditing and benchmarking.
    """
    
    DEFAULT_RUBRIC_WEIGHTS = {
        "concept_blueprint": 0.30,
        "algorithm_correctness": 0.25,
        "reasoning": 0.15,
        "time_complexity": 0.15,
        "space_complexity": 0.10,
        "edge_cases": 0.05
    }

    @classmethod
    def calculate_blueprint_score(
        cls, 
        eval_concepts: List[ConceptStatusEvaluation], 
        blueprint: ConceptBlueprint
    ) -> float:
        """
        Calculates the weighted score across all concepts defined in the Concept Blueprint.
        Returns a percentage value from 0.0 to 100.0.
        """
        concept_weights = {c.concept_id: c.weight for c in blueprint.concepts}
        total_weight = sum(concept_weights.values())
        
        if total_weight <= 0:
            return 0.0
            
        accumulated_score = 0.0
        eval_map = {c.concept_id: c.score for c in eval_concepts}
        
        for c in blueprint.concepts:
            score = eval_map.get(c.concept_id, 0.0)
            # Ensure score is strictly bounded in [0.0, 0.5, 1.0]
            bounded_score = min(max(float(score), 0.0), 1.0)
            weight = concept_weights.get(c.concept_id, 10.0)
            accumulated_score += (bounded_score * weight)
            
        blueprint_percentage = (accumulated_score / total_weight) * 100.0
        return round(blueprint_percentage, 2)

    @classmethod
    def calculate_final_score(
        cls,
        gemini_eval: GeminiEvaluationSchema,
        blueprint: ConceptBlueprint,
        custom_rubric_weights: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Calculates final deterministic score and dimension breakdown.
        """
        weights = custom_rubric_weights or cls.DEFAULT_RUBRIC_WEIGHTS
        
        # 1. Blueprint concept percentage (0 - 100)
        blueprint_pct = cls.calculate_blueprint_score(gemini_eval.concepts, blueprint)
        
        # 2. Dimensions normalized to 0 - 100
        algo_score = min(max(gemini_eval.algorithm_correctness, 0.0), 1.0) * 100.0
        reasoning_score = min(max(gemini_eval.reasoning, 0.0), 1.0) * 100.0
        time_score = min(max(gemini_eval.time_complexity.score, 0.0), 1.0) * 100.0
        space_score = min(max(gemini_eval.space_complexity.score, 0.0), 1.0) * 100.0
        edge_score = min(max(gemini_eval.edge_cases, 0.0), 1.0) * 100.0

        dimension_scores = {
            "concept_blueprint": round(blueprint_pct, 1),
            "algorithm_correctness": round(algo_score, 1),
            "reasoning": round(reasoning_score, 1),
            "time_complexity": round(time_score, 1),
            "space_complexity": round(space_score, 1),
            "edge_cases": round(edge_score, 1)
        }

        # 3. Final weighted calculation
        raw_final_score = (
            (blueprint_pct * weights["concept_blueprint"]) +
            (algo_score * weights["algorithm_correctness"]) +
            (reasoning_score * weights["reasoning"]) +
            (time_score * weights["time_complexity"]) +
            (space_score * weights["space_complexity"]) +
            (edge_score * weights["edge_cases"])
        )
        
        final_score = round(min(max(raw_final_score, 0.0), 100.0), 1)

        return {
            "final_score": final_score,
            "blueprint_score": blueprint_pct,
            "dimension_scores": dimension_scores
        }
