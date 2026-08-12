from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SubmissionCreate(BaseModel):
    student_answer: str = Field(..., min_length=10, max_length=10000)

class SubmissionSummary(BaseModel):
    id: str
    question_id: str
    question_title: str
    category: str
    difficulty: str
    final_score: float
    created_at: str

class SubmissionDetail(BaseModel):
    id: str
    user_id: str
    question_id: str
    question_version_id: str
    student_answer: str
    final_score: float
    status: str
    created_at: str
    evaluation: Optional[Dict[str, Any]] = None
