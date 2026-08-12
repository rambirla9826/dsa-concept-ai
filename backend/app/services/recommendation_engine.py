from typing import List, Dict, Any
from app.core.db import db

class RecommendationEngine:
    """
    Analyzes user concept scores, topic mastery levels, and submission history to recommend
    the next best questions for targeted skill improvement.
    """
    
    @classmethod
    def get_recommendations_for_user(cls, user_id: str, limit: int = 5) -> Dict[str, Any]:
        user_doc = db.get_document("users", user_id)
        if not user_doc:
            user_doc = {}
            
        metrics = user_doc.get("metrics", {})
        topic_scores = metrics.get("topic_scores", {})
        
        # All available questions
        all_questions = db.list_collection("questions")
        published_questions = [q for q in all_questions if q.get("is_published", True)]
        
        # User completed questions
        submissions = db.query_collection("submissions", "user_id", user_id)
        completed_q_ids = {s.get("question_id") for s in submissions if s.get("final_score", 0) >= 70}
        
        # Identify weak categories (score < 70 or unattempted)
        weak_topics = sorted(
            topic_scores.items(), key=lambda x: x[1]
        )
        weak_category_names = [t[0] for t in weak_topics if t[1] < 70]
        
        # Filter uncompleted questions prioritized by weak categories
        recommended = []
        for q in published_questions:
            if q.get("id") not in completed_q_ids:
                category = q.get("category", "")
                priority = 10 if category in weak_category_names else 5
                recommended.append((priority, q))
                
        # Sort recommendations by priority (weakest topics first)
        recommended.sort(key=lambda x: x[0], reverse=True)
        recommended_questions = [q[1] for q in recommended[:limit]]
        
        # Top 3 weak categories & strong categories
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1])
        weak_topics_list = [{"category": t[0], "score": round(t[1], 1)} for t in sorted_topics if t[1] < 70][:3]
        strong_topics_list = [{"category": t[0], "score": round(t[1], 1)} for t in reversed(sorted_topics) if t[1] >= 70][:3]
        
        return {
            "recommended_questions": [
                {
                    "id": q.get("id"),
                    "title": q.get("title"),
                    "category": q.get("category"),
                    "difficulty": q.get("difficulty")
                }
                for q in recommended_questions
            ],
            "weak_topics": weak_topics_list,
            "strong_topics": strong_topics_list
        }
