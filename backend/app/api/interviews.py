from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends
from app.core.db import db
from app.core.security import get_current_user
from app.models.interview import (
    InterviewStartResponse, QuestionGenerated, QuestionAnswerSubmit,
    QuestionEvaluationResult, InterviewReport, StudyRecommendationItem
)
from app.services.interview_engine import InterviewEngine
from app.services.interview_evaluator import InterviewEvaluator

router = APIRouter(prefix="/interviews", tags=["AI Voice Interview"])

@router.post("/start", response_model=dict)
def start_interview(current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]
    
    # 1. Fetch user's latest resume
    user_resumes = db.query_collection("resumes", "user_id", user_id)
    if not user_resumes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload your resume before starting an AI Voice Technical Interview."
        )
    user_resumes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    latest_resume = user_resumes[0]

    # 2. Atomic Attempt Reservation Check Lock
    try:
        limit_info = InterviewEngine.check_and_reserve_attempt(user_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err))

    # 3. Create Interview Session
    interview_id = f"int_{uuid.uuid4().hex[:10]}"
    now_str = datetime.now(timezone.utc).isoformat()
    
    interview_doc = {
        "id": interview_id,
        "user_id": user_id,
        "resume_id": latest_resume["id"],
        "status": "IN_PROGRESS",
        "total_questions": 5,
        "completed_questions": 0,
        "overall_score": 0.0,
        "topic_scores": {},
        "created_at": now_str
    }
    db.set_document("interviews", interview_id, interview_doc)

    return {
        "interview_id": interview_id,
        "allowed_interviews": limit_info["allowed_interviews"],
        "used_interviews": limit_info["used_interviews"],
        "remaining_interviews": limit_info["remaining_interviews"],
        "resume_topics": latest_resume.get("skills", [])
    }

@router.get("/{id}/next-question", response_model=dict)
def get_next_question(id: str, current_user: dict = Depends(get_current_user)):
    interview = db.get_document("interviews", id)
    if not interview or interview.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=404, detail="Interview session not found.")
        
    if interview.get("status") == "COMPLETED":
        raise HTTPException(status_code=400, detail="Interview session already completed.")

    current_q_num = interview.get("completed_questions", 0) + 1
    if current_q_num > interview.get("total_questions", 5):
        raise HTTPException(status_code=400, detail="All questions completed. Call /finish to generate report.")

    resume_doc = db.get_document("resumes", interview.get("resume_id")) or {}
    
    # Previous evaluations for this interview
    iqs = db.query_collection("interview_questions", "interview_id", id)
    iqs.sort(key=lambda x: x.get("question_number", 0))

    generated = InterviewEngine.generate_next_question(
        user_id=current_user["uid"],
        interview_id=id,
        resume_doc=resume_doc,
        current_question_number=current_q_num,
        previous_evaluations=iqs
    )

    # Store Question Record
    now_str = datetime.now(timezone.utc).isoformat()
    iq_doc = {
        "id": generated.question_id,
        "interview_id": id,
        "user_id": current_user["uid"],
        "question_number": generated.question_number,
        "question_text": generated.question_text,
        "topic": generated.topic,
        "difficulty": generated.difficulty,
        "question_type": generated.question_type,
        "student_answer_raw": "",
        "eval_score": 0.0,
        "asked_at": now_str
    }
    db.set_document("interview_questions", generated.question_id, iq_doc)

    return generated.model_dump()

@router.post("/{id}/submit-answer", response_model=dict)
def submit_interview_answer(
    id: str,
    payload: QuestionAnswerSubmit,
    current_user: dict = Depends(get_current_user)
):
    interview = db.get_document("interviews", id)
    if not interview or interview.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    # Get latest active question
    iqs = db.query_collection("interview_questions", "interview_id", id)
    iqs.sort(key=lambda x: x.get("question_number", 0), reverse=True)
    if not iqs:
        raise HTTPException(status_code=400, detail="No active question found for this interview.")
        
    latest_q = iqs[0]
    
    # Grade Answer via Structured Technical Evaluator
    eval_result = InterviewEvaluator.evaluate_question_answer(
        question_text=latest_q["question_text"],
        topic=latest_q["topic"],
        student_answer=payload.student_answer
    )
    eval_result.question_id = latest_q["id"]

    # Store Evaluation Record
    eval_id = f"ie_{uuid.uuid4().hex[:10]}"
    now_str = datetime.now(timezone.utc).isoformat()
    eval_doc = {
        "id": eval_id,
        "question_id": latest_q["id"],
        "interview_id": id,
        "dimension_scores": {
            "technical_correctness": eval_result.technical_correctness,
            "concept_understanding": eval_result.concept_understanding,
            "reasoning": eval_result.reasoning,
            "completeness": eval_result.completeness,
            "practical_understanding": eval_result.practical_understanding
        },
        "missing_concepts": eval_result.missing_concepts,
        "technical_feedback": eval_result.technical_feedback,
        "question_score": eval_result.question_score,
        "evaluator_model": "gemini-1.5-flash",
        "rubric_version": "v1.0",
        "evaluated_at": now_str
    }
    db.set_document("interview_evaluations", eval_id, eval_doc)

    # Update Question Record with student answer and score
    db.update_document("interview_questions", latest_q["id"], {
        "student_answer_raw": payload.student_answer,
        "eval_score": eval_result.question_score,
        "evaluation_id": eval_id
    })

    # Increment completed questions count in session
    completed_q = interview.get("completed_questions", 0) + 1
    db.update_document("interviews", id, {"completed_questions": completed_q})

    return {
        "question_id": latest_q["id"],
        "question_score": eval_result.question_score,
        "evaluation": eval_result.model_dump()
    }

@router.post("/{id}/finish", response_model=dict)
def finish_interview(id: str, current_user: dict = Depends(get_current_user)):
    interview = db.get_document("interviews", id)
    if not interview or interview.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    iqs = db.query_collection("interview_questions", "interview_id", id)
    if not iqs:
        raise HTTPException(status_code=400, detail="Cannot finish an empty interview session.")

    # Calculate Topic Scores and Overall Performance
    topic_scores = {}
    topic_counts = {}
    all_scores = []
    
    for q in iqs:
        score = q.get("eval_score", 0.0)
        topic = q.get("topic", "General")
        all_scores.append(score)
        
        topic_scores[topic] = topic_scores.get(topic, 0.0) + score
        topic_counts[topic] = topic_counts.get(topic, 0) + 1

    topic_averages = {t: round(topic_scores[t] / topic_counts[t], 1) for t in topic_scores}
    overall_score = round(sum(all_scores) / max(1, len(all_scores)), 1)
    
    sorted_topics = sorted(topic_averages.items(), key=lambda x: x[1], reverse=True)
    strong_areas = [t[0] for t in sorted_topics if t[1] >= 70.0]
    weak_areas = [t[0] for t in sorted_topics if t[1] < 70.0]
    if not strong_areas and sorted_topics:
        strong_areas = [sorted_topics[0][0]]

    # Generate Exact Study Recommendations
    recommendations = InterviewEvaluator.generate_exact_study_recommendations(topic_averages)

    now_str = datetime.now(timezone.utc).isoformat()
    db.update_document("interviews", id, {
        "status": "COMPLETED",
        "overall_score": overall_score,
        "topic_scores": topic_averages,
        "strong_areas": strong_areas,
        "weak_areas": weak_areas,
        "study_recommendations": [r.model_dump() for r in recommendations],
        "completed_at": now_str
    })

    return {
        "interview_id": id,
        "overall_score": overall_score,
        "topic_scores": topic_averages,
        "strong_areas": strong_areas,
        "weak_areas": weak_areas,
        "study_recommendations": [r.model_dump() for r in recommendations],
        "completed_at": now_str
    }

@router.get("/{id}/report", response_model=dict)
def get_interview_report(id: str, current_user: dict = Depends(get_current_user)):
    interview = db.get_document("interviews", id)
    if not interview or (current_user["role"] != "ADMIN" and interview.get("user_id") != current_user["uid"]):
        raise HTTPException(status_code=404, detail="Interview report not found.")

    iqs = db.query_collection("interview_questions", "interview_id", id)
    iqs.sort(key=lambda x: x.get("question_number", 0))

    # User's score progression over past interviews
    user_interviews = db.query_collection("interviews", "user_id", interview.get("user_id"))
    completed_history = [
        {
            "interview_id": i["id"],
            "score": i.get("overall_score", 0.0),
            "date": i.get("completed_at", i.get("created_at"))
        }
        for i in user_interviews if i.get("status") == "COMPLETED"
    ]
    completed_history.sort(key=lambda x: x["date"])

    return {
        "interview": interview,
        "questions": iqs,
        "history_progress": completed_history
    }

@router.get("/history", response_model=List[dict])
def get_user_interview_history(current_user: dict = Depends(get_current_user)):
    user_interviews = db.query_collection("interviews", "user_id", current_user["uid"])
    user_interviews.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return user_interviews
