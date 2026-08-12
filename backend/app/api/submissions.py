from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from app.core.db import db
from app.core.security import get_current_user
from app.models.submission import SubmissionCreate
from app.models.question import QuestionDetail, ConceptBlueprint
from app.services.gemini_evaluator import GeminiEvaluator
from app.services.scoring_engine import ScoringEngine

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.post("/question/{question_id}", response_model=dict)
def submit_answer(
    question_id: str,
    payload: SubmissionCreate,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["uid"]
    
    # 1. Fetch Question
    q_doc = db.get_document("questions", question_id)
    if not q_doc:
        raise HTTPException(status_code=404, detail="Question not found")
        
    version_id = q_doc.get("current_version_id")
    
    # 2. Fetch Concept Blueprint
    blueprints = db.list_collection("concept_blueprints")
    blueprint_doc = None
    for bp in blueprints:
        if bp.get("question_version_id") == version_id:
            blueprint_doc = bp
            break
            
    if not blueprint_doc:
        raise HTTPException(status_code=404, detail="Concept Blueprint missing for question version")

    question_obj = QuestionDetail(**q_doc)
    blueprint_obj = ConceptBlueprint(**blueprint_doc)

    # 3. Invoke Gemini Evaluation Pipeline
    try:
        gemini_eval = GeminiEvaluator.evaluate(
            question=question_obj,
            blueprint=blueprint_obj,
            student_answer=payload.student_answer
        )
    except Exception as e:
        print(f"[Submission API Error] Evaluation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Evaluation temporarily unavailable. Please try again."
        )

    # 4. Calculate Deterministic Final Score
    scoring_result = ScoringEngine.calculate_final_score(
        gemini_eval=gemini_eval,
        blueprint=blueprint_obj
    )

    submission_id = f"sub_{uuid.uuid4().hex[:12]}"
    evaluation_id = f"eval_{uuid.uuid4().hex[:12]}"
    now_str = datetime.now(timezone.utc).isoformat()

    # 5. Store Evaluation Document
    eval_doc = {
        "id": evaluation_id,
        "submission_id": submission_id,
        "user_id": user_id,
        "question_id": question_id,
        "final_score": scoring_result["final_score"],
        "blueprint_score": scoring_result["blueprint_score"],
        "dimension_scores": scoring_result["dimension_scores"],
        "concept_evaluations": [c.model_dump() for c in gemini_eval.concepts],
        "algorithm_correctness": gemini_eval.algorithm_correctness,
        "reasoning": gemini_eval.reasoning,
        "time_complexity": gemini_eval.time_complexity.model_dump(),
        "space_complexity": gemini_eval.space_complexity.model_dump(),
        "edge_cases": gemini_eval.edge_cases,
        "technical_feedback": gemini_eval.technical_feedback,
        "misconceptions": gemini_eval.misconceptions,
        "strengths": gemini_eval.strengths,
        "improvements": gemini_eval.improvements,
        "evaluator_model": "gemini-1.5-flash",
        "evaluator_prompt_version": "v1.0",
        "rubric_version": "v1.0",
        "evaluated_at": now_str
    }
    db.set_document("evaluations", evaluation_id, eval_doc)

    # 6. Store Submission Document
    sub_doc = {
        "id": submission_id,
        "user_id": user_id,
        "question_id": question_id,
        "question_title": q_doc.get("title"),
        "question_version_id": version_id,
        "blueprint_id": blueprint_doc.get("id"),
        "student_answer": payload.student_answer,
        "status": "EVALUATED",
        "evaluation_id": evaluation_id,
        "final_score": scoring_result["final_score"],
        "created_at": now_str
    }
    db.set_document("submissions", submission_id, sub_doc)

    # 7. Update User Performance Metrics & Topic Scores
    user_doc = db.get_document("users", user_id)
    if user_doc:
        metrics = user_doc.get("metrics", {})
        total_attempted = metrics.get("total_attempted", 0) + 1
        
        # Calculate new user average score
        all_user_subs = db.query_collection("submissions", "user_id", user_id)
        scores = [s.get("final_score", 0.0) for s in all_user_subs]
        avg_score = round(sum(scores) / len(scores), 1) if scores else scoring_result["final_score"]
        
        # Topic score update
        category = q_doc.get("category", "General")
        topic_scores = metrics.get("topic_scores", {})
        category_subs = [s.get("final_score", 0.0) for s in all_user_subs if db.get_document("questions", s.get("question_id", "")) and db.get_document("questions", s.get("question_id", "")).get("category") == category]
        category_avg = round(sum(category_subs) / max(1, len(category_subs)), 1) if category_subs else scoring_result["final_score"]
        topic_scores[category] = category_avg
        
        metrics["total_attempted"] = total_attempted
        metrics["total_completed"] = sum(1 for s in scores if s >= 70.0)
        metrics["average_score"] = avg_score
        metrics["topic_scores"] = topic_scores
        
        db.update_document("users", user_id, {"metrics": metrics})

    # Log AI usage entry
    ai_log_id = f"ailog_{uuid.uuid4().hex[:12]}"
    db.set_document("ai_usage", ai_log_id, {
        "id": ai_log_id,
        "timestamp": now_str,
        "user_id": user_id,
        "question_id": question_id,
        "status": "SUCCESS",
        "model": "gemini-1.5-flash"
    })

    return {
        "submission_id": submission_id,
        "evaluation_id": evaluation_id,
        "final_score": scoring_result["final_score"],
        "evaluation": eval_doc
    }

@router.get("/{id}", response_model=dict)
def get_submission_result(id: str, current_user: dict = Depends(get_current_user)):
    sub_doc = db.get_document("submissions", id)
    if not sub_doc:
        raise HTTPException(status_code=404, detail="Submission not found")
        
    if current_user["role"] != "ADMIN" and sub_doc.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Access denied to private submission")
        
    eval_id = sub_doc.get("evaluation_id")
    eval_doc = db.get_document("evaluations", eval_id) if eval_id else None
    
    q_doc = db.get_document("questions", sub_doc.get("question_id"))
    
    return {
        "submission": sub_doc,
        "evaluation": eval_doc,
        "question": q_doc
    }

@router.get("", response_model=List[dict])
def list_user_submissions(current_user: dict = Depends(get_current_user)):
    user_subs = db.query_collection("submissions", "user_id", current_user["uid"])
    user_subs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return user_subs
