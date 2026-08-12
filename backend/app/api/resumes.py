from datetime import datetime, timezone
import uuid
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from app.core.db import db
from app.core.security import get_current_user
from app.services.resume_analyzer import ResumeAnalyzer

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=dict)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["uid"]
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resume files are supported initially."
        )

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Parse text and extract topics
    extracted_text = ResumeAnalyzer.extract_text_from_pdf(content)
    parsed_data = ResumeAnalyzer.analyze_resume_text(extracted_text)

    resume_id = f"res_{uuid.uuid4().hex[:10]}"
    now_str = datetime.now(timezone.utc).isoformat()

    resume_doc = {
        "id": resume_id,
        "user_id": user_id,
        "filename": file.filename,
        "skills": parsed_data.skills,
        "languages": parsed_data.languages,
        "frameworks": parsed_data.frameworks,
        "databases": parsed_data.databases,
        "cloud": parsed_data.cloud,
        "projects": [p.model_dump() for p in parsed_data.projects],
        "experience": parsed_data.experience,
        "certifications": parsed_data.certifications,
        "compact_context": parsed_data.compact_context,
        "created_at": now_str
    }
    db.set_document("resumes", resume_id, resume_doc)

    return {
        "resume_id": resume_id,
        "filename": file.filename,
        "extracted_skills": parsed_data.skills,
        "extracted_projects": [p.name for p in parsed_data.projects],
        "compact_context": parsed_data.compact_context
    }

@router.get("/latest", response_model=dict)
def get_latest_resume(current_user: dict = Depends(get_current_user)):
    user_resumes = db.query_collection("resumes", "user_id", current_user["uid"])
    if not user_resumes:
        raise HTTPException(status_code=404, detail="No uploaded resume found for active user.")
        
    user_resumes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    latest = user_resumes[0]
    return latest
