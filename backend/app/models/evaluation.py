from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ConceptStatusEvaluation(BaseModel):
    concept_id: str
    status: str  # "correct", "partial", "incorrect"
    score: float  # 1.0, 0.5, 0.0
    evidence: str
    feedback: Optional[str] = None

class ComplexityEvaluation(BaseModel):
    student_answer: str
    expected: str
    score: float  # 0.0 to 1.0
    feedback: Optional[str] = None

class GeminiEvaluationSchema(BaseModel):
    concepts: List[ConceptStatusEvaluation]
    algorithm_correctness: float  # 0.0 to 1.0
    reasoning: float              # 0.0 to 1.0
    time_complexity: ComplexityEvaluation
    space_complexity: ComplexityEvaluation
    edge_cases: float             # 0.0 to 1.0
    technical_feedback: str
    misconceptions: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)

class FullEvaluationResult(BaseModel):
    id: str
    submission_id: str
    user_id: str
    question_id: str
    final_score: float  # 0.0 to 100.0
    blueprint_score: float  # 0.0 to 100.0
    dimension_scores: Dict[str, float]
    concept_evaluations: List[ConceptStatusEvaluation]
    algorithm_correctness: float
    reasoning: float
    time_complexity: ComplexityEvaluation
    space_complexity: ComplexityEvaluation
    edge_cases: float
    technical_feedback: str
    misconceptions: List[str]
    strengths: List[str]
    improvements: List[str]
    evaluator_model: str
    evaluator_prompt_version: str
    rubric_version: str
    evaluated_at: str
