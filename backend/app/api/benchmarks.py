from datetime import datetime, timezone
import uuid
import math
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.core.db import db
from app.core.security import require_admin

router = APIRouter(prefix="/admin/benchmarks", tags=["Human Benchmark System"], dependencies=[Depends(require_admin)])

class BenchmarkEntryCreate(BaseModel):
    submission_id: str
    human_score: float
    notes: str = ""

@router.post("", response_model=dict)
def record_human_benchmark(payload: BenchmarkEntryCreate):
    sub_doc = db.get_document("submissions", payload.submission_id)
    if not sub_doc:
        raise HTTPException(status_code=404, detail="Submission not found")
        
    bench_id = f"bm_{uuid.uuid4().hex[:10]}"
    entry = {
        "id": bench_id,
        "submission_id": payload.submission_id,
        "question_id": sub_doc.get("question_id"),
        "student_answer": sub_doc.get("student_answer"),
        "ai_score": sub_doc.get("final_score", 0.0),
        "human_score": payload.human_score,
        "notes": payload.notes,
        "recorded_at": datetime.now(timezone.utc).isoformat()
    }
    db.set_document("benchmarks", bench_id, entry)
    return {"message": "Human benchmark recorded", "benchmark_id": bench_id}

@router.get("", response_model=dict)
def get_benchmark_analytics():
    benchmarks = db.list_collection("benchmarks")
    if not benchmarks:
        return {
            "total_benchmarks": 0,
            "mean_absolute_error": 0.0,
            "agreement_rate_pct": 100.0,
            "correlation": 1.0,
            "entries": []
        }
        
    ai_scores = [b["ai_score"] for b in benchmarks]
    human_scores = [b["human_score"] for b in benchmarks]
    n = len(benchmarks)
    
    # 1. Mean Absolute Error (MAE)
    mae = sum(abs(a - h) for a, h in zip(ai_scores, human_scores)) / n
    
    # 2. Agreement Rate (Within 10 points threshold)
    agreed = sum(1 for a, h in zip(ai_scores, human_scores) if abs(a - h) <= 10.0)
    agreement_pct = round((agreed / n) * 100, 1)

    # 3. Pearson Correlation
    mean_a = sum(ai_scores) / n
    mean_h = sum(human_scores) / n
    num = sum((a - mean_a) * (h - mean_h) for a, h in zip(ai_scores, human_scores))
    den = math.sqrt(sum((a - mean_a)**2 for a in ai_scores) * sum((h - mean_h)**2 for h in human_scores))
    corr = round(num / den, 3) if den != 0 else 1.0

    return {
        "total_benchmarks": n,
        "mean_absolute_error": round(mae, 2),
        "agreement_rate_pct": agreement_pct,
        "correlation": corr,
        "entries": benchmarks
    }
