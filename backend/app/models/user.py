from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    display_name: str
    role: Optional[str] = "USER"  # "USER" or "ADMIN"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    uid: str
    email: str
    display_name: str
    role: str
    created_at: str
    last_login: str
    streak_count: int = 0
    last_active_date: Optional[str] = None
    is_disabled: bool = False
    metrics: Dict[str, Any] = Field(default_factory=lambda: {
        "total_attempted": 0,
        "total_completed": 0,
        "average_score": 0.0,
        "topic_scores": {}
    })
