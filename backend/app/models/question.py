from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ConceptItem(BaseModel):
    concept_id: str
    concept_name: str
    description: str
    importance: str = "medium"  # "high", "medium", "low"
    weight: float = 10.0
    is_mandatory: bool = True
    expected_keywords: Optional[List[str]] = None

class ConceptBlueprint(BaseModel):
    id: str
    question_version_id: str
    concepts: List[ConceptItem]
    expected_time_complexity: str
    expected_space_complexity: str
    expected_edge_cases: List[str] = Field(default_factory=list)

class ExampleCase(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None

class QuestionCreate(BaseModel):
    title: str
    category: str
    difficulty: str  # "Easy", "Medium", "Hard"
    problem_statement: str
    examples: List[ExampleCase]
    constraints: List[str]
    hints: List[str] = Field(default_factory=list)
    concepts: List[ConceptItem]
    expected_time_complexity: str
    expected_space_complexity: str
    expected_edge_cases: List[str] = Field(default_factory=list)

class QuestionSummary(BaseModel):
    id: str
    title: str
    category: str
    difficulty: str
    is_published: bool
    created_at: str

class QuestionDetail(BaseModel):
    id: str
    title: str
    category: str
    difficulty: str
    problem_statement: str
    examples: List[ExampleCase]
    constraints: List[str]
    hints: List[str]
    current_version_id: str
    blueprint: Optional[ConceptBlueprint] = None
