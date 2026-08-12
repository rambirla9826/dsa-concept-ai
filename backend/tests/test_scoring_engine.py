import pytest
from app.services.scoring_engine import ScoringEngine
from app.models.evaluation import GeminiEvaluationSchema, ConceptStatusEvaluation, ComplexityEvaluation
from app.models.question import ConceptBlueprint, ConceptItem

def build_mock_blueprint():
    return ConceptBlueprint(
        id="bp_test",
        question_version_id="qv_test",
        concepts=[
            ConceptItem(concept_id="C1", concept_name="Prerequisite Sorted Array", description="Sorted array required", weight=30.0, is_mandatory=True),
            ConceptItem(concept_id="C2", concept_name="Two Pointers Initialization", description="Left and Right boundary", weight=30.0, is_mandatory=True),
            ConceptItem(concept_id="C3", concept_name="Middle Comparison", description="Mid point check", weight=40.0, is_mandatory=True)
        ],
        expected_time_complexity="O(log n)",
        expected_space_complexity="O(1)",
        expected_edge_cases=["Empty array"]
    )

def test_perfect_concept_score():
    blueprint = build_mock_blueprint()
    concepts = [
        ConceptStatusEvaluation(concept_id="C1", status="correct", score=1.0, evidence="Array is sorted"),
        ConceptStatusEvaluation(concept_id="C2", status="correct", score=1.0, evidence="Left=0, Right=n-1"),
        ConceptStatusEvaluation(concept_id="C3", status="correct", score=1.0, evidence="mid = (left+right)//2")
    ]
    bp_score = ScoringEngine.calculate_blueprint_score(concepts, blueprint)
    assert bp_score == 100.0

def test_partial_concept_score():
    blueprint = build_mock_blueprint()
    concepts = [
        ConceptStatusEvaluation(concept_id="C1", status="correct", score=1.0, evidence="Array is sorted"),
        ConceptStatusEvaluation(concept_id="C2", status="partial", score=0.5, evidence="Mentions pointers"),
        ConceptStatusEvaluation(concept_id="C3", status="incorrect", score=0.0, evidence="No mid point mentioned")
    ]
    # C1 (30*1.0) + C2 (30*0.5) + C3 (40*0) = 30 + 15 + 0 = 45 out of 100
    bp_score = ScoringEngine.calculate_blueprint_score(concepts, blueprint)
    assert bp_score == 45.0

def test_final_score_determinism():
    blueprint = build_mock_blueprint()
    gemini_eval = GeminiEvaluationSchema(
        concepts=[
            ConceptStatusEvaluation(concept_id="C1", status="correct", score=1.0, evidence=""),
            ConceptStatusEvaluation(concept_id="C2", status="correct", score=1.0, evidence=""),
            ConceptStatusEvaluation(concept_id="C3", status="correct", score=1.0, evidence="")
        ],
        algorithm_correctness=1.0,
        reasoning=1.0,
        time_complexity=ComplexityEvaluation(student_answer="O(log n)", expected="O(log n)", score=1.0),
        space_complexity=ComplexityEvaluation(student_answer="O(1)", expected="O(1)", score=1.0),
        edge_cases=1.0,
        technical_feedback="Excellent",
        misconceptions=[],
        strengths=["Perfect understanding"],
        improvements=[]
    )
    result1 = ScoringEngine.calculate_final_score(gemini_eval, blueprint)
    result2 = ScoringEngine.calculate_final_score(gemini_eval, blueprint)
    
    assert result1["final_score"] == 100.0
    assert result1["final_score"] == result2["final_score"]
    assert result1["blueprint_score"] == result2["blueprint_score"]
