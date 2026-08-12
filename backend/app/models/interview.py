from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ProjectTechDetail(BaseModel):
    name: str
    technologies: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)

class ResumeDataSchema(BaseModel):
    skills: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    cloud: List[str] = Field(default_factory=list)
    projects: List[ProjectTechDetail] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    compact_context: str = ""

class ResumeRecord(BaseModel):
    id: str
    user_id: str
    filename: str
    skills: List[str]
    projects: List[Dict[str, Any]]
    compact_context: str
    created_at: str

class InterviewStartResponse(BaseModel):
    interview_id: str
    allowed_interviews: int
    used_interviews: int
    remaining_interviews: int
    resume_topics: List[str]

class QuestionGenerated(BaseModel):
    question_id: str
    question_number: int
    question_text: str
    topic: str
    difficulty: str
    question_type: str

class QuestionAnswerSubmit(BaseModel):
    student_answer: str = Field(..., min_length=2)

class QuestionEvaluationResult(BaseModel):
    question_id: str
    technical_correctness: float  # 0.0 to 1.0
    concept_understanding: float # 0.0 to 1.0
    reasoning: float             # 0.0 to 1.0
    completeness: float          # 0.0 to 1.0
    practical_understanding: float # 0.0 to 1.0
    missing_concepts: List[str] = Field(default_factory=list)
    technical_feedback: str
    question_score: float        # 0.0 to 100.0

class StudyRecommendationItem(BaseModel):
    topic: str
    score: float
    exact_concepts: List[str]

class InterviewReport(BaseModel):
    interview_id: str
    user_id: str
    overall_score: float
    project_knowledge_score: float
    technical_knowledge_scores: Dict[str, float]
    concept_breakdown: Dict[str, Dict[str, float]]
    strong_areas: List[str]
    weak_areas: List[str]
    study_recommendations: List[StudyRecommendationItem]
    history_progress: List[Dict[str, Any]] = Field(default_factory=list)
    completed_at: str

class AdminLimitUpdate(BaseModel):
    allowed_interviews: int = Field(..., ge=0)
    is_unlimited: bool = False
    is_disabled: bool = False

class AdminRubricConfig(BaseModel):
    technical_correctness_weight: float = 0.40
    concept_understanding_weight: float = 0.25
    reasoning_weight: float = 0.15
    completeness_weight: float = 0.10
    practical_understanding_weight: float = 0.10
    default_allowed_interviews: int = 5
    questions_per_interview: int = 5
