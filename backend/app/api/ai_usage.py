from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from app.core.db import db
from app.core.security import require_admin
from app.config import settings

router = APIRouter(prefix="/admin/ai-usage", tags=["AI Usage Analytics"], dependencies=[Depends(require_admin)])

@router.get("", response_model=dict)
def get_ai_usage_stats():
    logs = db.list_collection("ai_usage")
    today_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    month_prefix = datetime.now(timezone.utc).strftime("%Y-%m")
    
    evals_today = sum(1 for log in logs if log.get("timestamp", "").startswith(today_prefix))
    evals_month = sum(1 for log in logs if log.get("timestamp", "").startswith(month_prefix))
    total_evals = len(logs)
    
    errors = sum(1 for log in logs if log.get("status") == "ERROR")
    error_rate = round((errors / max(1, total_evals)) * 100, 1)

    return {
        "provider": "Google Gemini",
        "model": settings.GEMINI_MODEL,
        "daily_limit": settings.DAILY_FREE_EVAL_LIMIT,
        "evaluations_today": evals_today,
        "evaluations_this_month": evals_month,
        "total_evaluations": total_evals,
        "quota_remaining_today": max(0, settings.DAILY_FREE_EVAL_LIMIT - evals_today),
        "error_count": errors,
        "error_rate_percent": error_rate,
        "estimated_cost_usd": 0.0,  # Operating under Free Tier
        "free_tier_status": "ACTIVE_FREE_TIER"
    }
