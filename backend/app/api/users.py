from fastapi import APIRouter, HTTPException, Depends
from app.core.db import db
from app.core.security import get_current_user
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/users", tags=["Student Dashboard"])

@router.get("/me/dashboard", response_model=dict)
def get_student_dashboard(current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]
    user_doc = db.get_document("users", user_id)
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
        
    metrics = user_doc.get("metrics", {})
    topic_scores = metrics.get("topic_scores", {})
    
    # Calculate weak and strong topics
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1])
    weak_topics = [{"category": t[0], "score": round(t[1], 1)} for t in sorted_topics if t[1] < 70]
    strong_topics = [{"category": t[0], "score": round(t[1], 1)} for t in reversed(sorted_topics) if t[1] >= 70]

    # Recent submissions
    all_subs = db.query_collection("submissions", "user_id", user_id)
    all_subs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    recent_subs = all_subs[:5]

    # Recommendations
    recs = RecommendationEngine.get_recommendations_for_user(user_id, limit=4)

    return {
        "user_info": {
            "uid": user_doc["uid"],
            "display_name": user_doc.get("display_name"),
            "email": user_doc.get("email"),
            "streak_count": user_doc.get("streak_count", 1)
        },
        "stats": {
            "total_attempted": metrics.get("total_attempted", 0),
            "total_completed": metrics.get("total_completed", 0),
            "average_concept_score": round(metrics.get("average_score", 0.0), 1),
            "current_streak": user_doc.get("streak_count", 1)
        },
        "topic_performance": topic_scores,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "recommended_questions": recs["recommended_questions"],
        "recent_submissions": recent_subs
    }

@router.get("/me/recommendations", response_model=dict)
def get_recommendations(current_user: dict = Depends(get_current_user)):
    return RecommendationEngine.get_recommendations_for_user(current_user["uid"], limit=5)
