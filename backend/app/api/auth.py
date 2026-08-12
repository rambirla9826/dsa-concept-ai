from datetime import datetime, timezone
import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from app.core.db import db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import UserRegister, UserLogin, UserProfile

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
def register_user(payload: UserRegister):
    existing = db.query_collection("users", "email", payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered."
        )
    
    uid = f"usr_{uuid.uuid4().hex[:12]}"
    user_doc = {
        "uid": uid,
        "email": payload.email,
        "password": hash_password(payload.password),
        "display_name": payload.display_name,
        "role": "USER",  # Strictly locked to USER for public sign-up security!
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_login": datetime.now(timezone.utc).isoformat(),
        "streak_count": 1,
        "is_disabled": False,
        "metrics": {
            "total_attempted": 0,
            "total_completed": 0,
            "average_score": 0.0,
            "topic_scores": {}
        }
    }
    db.set_document("users", uid, user_doc)
    
    token = create_access_token(subject=uid, role=user_doc["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "uid": uid,
            "email": user_doc["email"],
            "display_name": user_doc["display_name"],
            "role": user_doc["role"]
        }
    }

@router.post("/login", response_model=dict)
def login_user(payload: UserLogin):
    matches = db.query_collection("users", "email", payload.email)
    if not matches:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    user_doc = matches[0]
    
    if user_doc.get("is_disabled", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account has been disabled. Contact system admin."
        )
        
    if not verify_password(payload.password, user_doc["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    # Update last login
    db.update_document("users", user_doc["uid"], {"last_login": datetime.now(timezone.utc).isoformat()})
    
    token = create_access_token(subject=user_doc["uid"], role=user_doc["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "uid": user_doc["uid"],
            "email": user_doc["email"],
            "display_name": user_doc["display_name"],
            "role": user_doc["role"]
        }
    }

@router.get("/me", response_model=dict)
def get_me(current_user: dict = Depends(get_current_user)):
    user_doc = db.get_document("users", current_user["uid"])
    if not user_doc:
        raise HTTPException(status_code=404, detail="User profile not found")
        
    return {
        "uid": user_doc["uid"],
        "email": user_doc["email"],
        "display_name": user_doc["display_name"],
        "role": user_doc["role"],
        "created_at": user_doc.get("created_at", ""),
        "last_login": user_doc.get("last_login", ""),
        "streak_count": user_doc.get("streak_count", 0),
        "metrics": user_doc.get("metrics", {})
    }
