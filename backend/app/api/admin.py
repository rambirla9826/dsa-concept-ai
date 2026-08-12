from datetime import datetime, timezone
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from app.core.db import db
from app.core.security import require_admin
from app.models.question import QuestionCreate

router = APIRouter(prefix="/admin", tags=["Admin Portal"], dependencies=[Depends(require_admin)])

@router.get("/overview", response_model=dict)
def get_admin_overview():
    users = db.list_collection("users")
    questions = db.list_collection("questions")
    submissions = db.list_collection("submissions")
    evaluations = db.list_collection("evaluations")
    
    total_users = len(users)
    total_questions = len(questions)
    total_submissions = len(submissions)
    
    scores = [s.get("final_score", 0.0) for s in submissions if "final_score" in s]
    avg_platform_score = round(sum(scores) / max(1, len(scores)), 1)
    
    # Category popularity
    category_counts = {}
    for q in questions:
        cat = q.get("category", "General")
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
    return {
        "metrics": {
            "total_users": total_users,
            "total_questions": total_questions,
            "total_submissions": total_submissions,
            "average_platform_score": avg_platform_score,
            "published_questions": sum(1 for q in questions if q.get("is_published", True))
        },
        "popular_categories": category_counts
    }

@router.post("/questions", response_model=dict)
def create_question(payload: QuestionCreate):
    q_id = f"q_{uuid.uuid4().hex[:8]}"
    v_id = f"{q_id}_v1"
    b_id = f"{q_id}_bp1"
    now_str = datetime.now(timezone.utc).isoformat()
    
    # Question Document
    q_doc = {
        "id": q_id,
        "title": payload.title,
        "slug": payload.title.lower().replace(" ", "-"),
        "category": payload.category,
        "difficulty": payload.difficulty,
        "problem_statement": payload.problem_statement,
        "examples": [e.model_dump() for e in payload.examples],
        "constraints": payload.constraints,
        "hints": payload.hints,
        "is_published": True,
        "current_version_id": v_id,
        "created_at": now_str,
        "updated_at": now_str
    }
    db.set_document("questions", q_id, q_doc)

    # Version Document
    v_doc = {
        "id": v_id,
        "question_id": q_id,
        "version_number": 1,
        "title": payload.title,
        "problem_statement": payload.problem_statement,
        "blueprint_id": b_id,
        "created_at": now_str
    }
    db.set_document("question_versions", v_id, v_doc)

    # Concept Blueprint Document
    b_doc = {
        "id": b_id,
        "question_version_id": v_id,
        "concepts": [c.model_dump() for c in payload.concepts],
        "expected_time_complexity": payload.expected_time_complexity,
        "expected_space_complexity": payload.expected_space_complexity,
        "expected_edge_cases": payload.expected_edge_cases
    }
    db.set_document("concept_blueprints", b_id, b_doc)

    return {
        "message": "Question and Concept Blueprint created successfully",
        "question_id": q_id,
        "version_id": v_id
    }

@router.put("/questions/{id}", response_model=dict)
def update_question(id: str, payload: QuestionCreate):
    existing_q = db.get_document("questions", id)
    if not existing_q:
        raise HTTPException(status_code=404, detail="Question not found")
        
    old_version_id = existing_q.get("current_version_id")
    # Fetch old version count to increment
    versions = db.query_collection("question_versions", "question_id", id)
    new_version_num = len(versions) + 1
    
    v_id = f"{id}_v{new_version_num}"
    b_id = f"{id}_bp{new_version_num}"
    now_str = datetime.now(timezone.utc).isoformat()
    
    # Update main question document (keeps original ID, updates version pointers)
    existing_q.update({
        "title": payload.title,
        "category": payload.category,
        "difficulty": payload.difficulty,
        "problem_statement": payload.problem_statement,
        "examples": [e.model_dump() for e in payload.examples],
        "constraints": payload.constraints,
        "hints": payload.hints,
        "current_version_id": v_id,
        "updated_at": now_str
    })
    db.set_document("questions", id, existing_q)

    # Create new Version Document (preserves history for past submissions)
    v_doc = {
        "id": v_id,
        "question_id": id,
        "version_number": new_version_num,
        "title": payload.title,
        "problem_statement": payload.problem_statement,
        "blueprint_id": b_id,
        "created_at": now_str
    }
    db.set_document("question_versions", v_id, v_doc)

    # Create new Concept Blueprint Document
    b_doc = {
        "id": b_id,
        "question_version_id": v_id,
        "concepts": [c.model_dump() for c in payload.concepts],
        "expected_time_complexity": payload.expected_time_complexity,
        "expected_space_complexity": payload.expected_space_complexity,
        "expected_edge_cases": payload.expected_edge_cases
    }
    db.set_document("concept_blueprints", b_id, b_doc)

    return {
        "message": f"Question updated to version {new_version_num}",
        "question_id": id,
        "new_version_id": v_id
    }

@router.delete("/questions/{id}", response_model=dict)
def archive_question(id: str):
    q_doc = db.get_document("questions", id)
    if not q_doc:
        raise HTTPException(status_code=404, detail="Question not found")
        
    db.update_document("questions", id, {"is_published": False})
    return {"message": "Question archived/unpublished successfully"}

@router.get("/users", response_model=List[dict])
def list_users():
    users = db.list_collection("users")
    sanitized = []
    for u in users:
        sanitized.append({
            "uid": u.get("uid"),
            "email": u.get("email"),
            "display_name": u.get("display_name"),
            "role": u.get("role"),
            "is_disabled": u.get("is_disabled", False),
            "created_at": u.get("created_at"),
            "metrics": u.get("metrics", {})
        })
    return sanitized

@router.put("/users/{uid}/status", response_model=dict)
def toggle_user_status(uid: str, is_disabled: bool):
    u = db.get_document("users", uid)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    if u.get("role") == "ADMIN":
        raise HTTPException(status_code=400, detail="Cannot disable administrative user accounts")
        
    db.update_document("users", uid, {"is_disabled": is_disabled})
    return {"message": f"User account status updated. Disabled: {is_disabled}"}

@router.put("/users/{uid}/role", response_model=dict)
def update_user_role(uid: str, new_role: str):
    if new_role not in ["USER", "ADMIN"]:
        raise HTTPException(status_code=400, detail="Role must be 'USER' or 'ADMIN'")
    u = db.get_document("users", uid)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    db.update_document("users", uid, {"role": new_role})
    return {"message": f"User role updated to {new_role}"}

@router.delete("/users/{uid}", response_model=dict)
def delete_user(uid: str):
    u = db.get_document("users", uid)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    if u.get("role") == "ADMIN":
        raise HTTPException(status_code=400, detail="Administrative accounts cannot be deleted directly")
    db.delete_document("users", uid)
    return {"message": f"User account {uid} permanently deleted"}

@router.get("/submissions", response_model=List[dict])
def list_all_submissions():
    subs = db.list_collection("submissions")
    subs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return subs

# --- ADMIN AI VOICE INTERVIEW CONTROLS & ANALYTICS ---

@router.get("/interviews/analytics", response_model=dict)
def get_admin_interview_analytics():
    interviews = db.list_collection("interviews")
    completed = [i for i in interviews if i.get("status") == "COMPLETED"]
    
    scores = [i.get("overall_score", 0.0) for i in completed]
    avg_score = round(sum(scores) / max(1, len(scores)), 1)
    
    # Weak topics across platform
    weak_counts = {}
    for i in completed:
        for topic in i.get("weak_areas", []):
            weak_counts[topic] = weak_counts.get(topic, 0) + 1
            
    sorted_weak = sorted(weak_counts.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_interviews": len(interviews),
        "completed_interviews": len(completed),
        "average_interview_score": avg_score,
        "most_common_weak_topics": [{"topic": t[0], "count": t[1]} for t in sorted_weak[:5]],
        "stt_error_count": 0
    }

@router.get("/interviews/limits", response_model=List[dict])
def list_interview_limits():
    limits = db.list_collection("interview_limits")
    users = db.list_collection("users")
    user_map = {u["uid"]: u for u in users}
    
    result = []
    for lim in limits:
        uid = lim.get("user_id")
        u_info = user_map.get(uid, {})
        result.append({
            "user_id": uid,
            "display_name": u_info.get("display_name", "User"),
            "email": u_info.get("email", ""),
            "allowed_interviews": lim.get("allowed_interviews", 5),
            "used_interviews": lim.get("used_interviews", 0),
            "is_unlimited": lim.get("is_unlimited", False),
            "is_disabled": lim.get("is_disabled", False),
            "updated_at": lim.get("updated_at", "")
        })
    return result

@router.put("/interviews/limits/{uid}", response_model=dict)
def update_user_interview_limit(uid: str, allowed_interviews: int, is_unlimited: bool = False, is_disabled: bool = False):
    u = db.get_document("users", uid)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
        
    limit_doc = db.get_document("interview_limits", uid) or {"user_id": uid, "used_interviews": 0}
    limit_doc.update({
        "allowed_interviews": allowed_interviews,
        "is_unlimited": is_unlimited,
        "is_disabled": is_disabled,
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    db.set_document("interview_limits", uid, limit_doc)

    # Audit Log
    audit_id = f"aud_{uuid.uuid4().hex[:10]}"
    db.set_document("audit_logs", audit_id, {
        "id": audit_id,
        "action": "UPDATE_INTERVIEW_LIMIT",
        "target_user_id": uid,
        "allowed_interviews": allowed_interviews,
        "is_unlimited": is_unlimited,
        "is_disabled": is_disabled,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    return {"message": "User interview limit updated successfully", "limit": limit_doc}

@router.post("/interviews/limits/{uid}/reset", response_model=dict)
def reset_user_interview_attempts(uid: str):
    limit_doc = db.get_document("interview_limits", uid)
    if not limit_doc:
        raise HTTPException(status_code=404, detail="Limit record not found for user")
        
    prev_used = limit_doc.get("used_interviews", 0)
    limit_doc["used_interviews"] = 0
    limit_doc["updated_at"] = datetime.now(timezone.utc).isoformat()
    db.set_document("interview_limits", uid, limit_doc)

    # Audit Log
    audit_id = f"aud_{uuid.uuid4().hex[:10]}"
    db.set_document("audit_logs", audit_id, {
        "id": audit_id,
        "action": "RESET_INTERVIEW_ATTEMPTS",
        "target_user_id": uid,
        "previous_used": prev_used,
        "new_used": 0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    return {"message": f"Interview attempts for user {uid} reset to 0 (Previous: {prev_used})"}

