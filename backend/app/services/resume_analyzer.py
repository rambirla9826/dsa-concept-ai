import re
import io
import json
from typing import Dict, Any, List
from app.config import settings
from app.models.interview import ResumeDataSchema, ProjectTechDetail

class ResumeAnalyzer:
    """
    Parses PDF resumes, extracts technical skills and project topics,
    and produces a compact context summary used for adaptive interview question generation.
    """
    
    SYSTEM_PROMPT = """
You are an expert technical recruiter and computer science interviewer.
Analyze the provided resume text and extract structured technical skills, project details, and core topics.

Extract into JSON format:
{
  "skills": ["Python", "FastAPI", "PostgreSQL", ...],
  "languages": ["Python", "C++", ...],
  "frameworks": ["FastAPI", "React", ...],
  "databases": ["PostgreSQL", "Qdrant", ...],
  "cloud": ["GCP", "AWS", ...],
  "projects": [
     {
       "name": "Project Name",
       "technologies": ["FastAPI", "Qdrant"],
       "topics": ["RAG", "Hybrid Search"]
     }
  ],
  "experience": ["Software Intern at TechCorp"],
  "certifications": ["AWS Developer"],
  "compact_context": "Compact 150-word technical summary of candidate skills and key project architectures."
}
"""

    @classmethod
    def extract_text_from_pdf(cls, file_bytes: bytes) -> str:
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        except Exception as e:
            print(f"[ResumeAnalyzer] PyPDF parsing failed: {e}. Falling back to plain text extraction.")
            try:
                return file_bytes.decode('utf-8', errors='ignore')
            except Exception:
                return "Sample Resume: Experience with Python, FastAPI, PostgreSQL, RAG, Qdrant, Data Structures, and System Design."

    @classmethod
    def analyze_resume_text(cls, text: str) -> ResumeDataSchema:
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(
                    model_name=settings.GEMINI_MODEL,
                    system_instruction=cls.SYSTEM_PROMPT
                )
                response = model.generate_content(
                    f"=== RESUME TEXT ===\n{text[:4000]}",
                    generation_config={"response_mime_type": "application/json", "temperature": 0.1}
                )
                raw_json = response.text.strip()
                if raw_json.startswith("```json"):
                    raw_json = raw_json.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_json)
                return ResumeDataSchema(**data)
            except Exception as e:
                print(f"[ResumeAnalyzer] Gemini extraction error: {e}. Using rule-based fallback parser.")

        return cls._rule_based_fallback_extraction(text)

    @classmethod
    def _rule_based_fallback_extraction(cls, text: str) -> ResumeDataSchema:
        text_lower = text.lower()
        
        # Skill dictionary
        all_skills_map = {
            "python": "Python", "java": "Java", "cpp": "C++", "c++": "C++", "javascript": "JavaScript",
            "typescript": "TypeScript", "sql": "SQL", "fastapi": "FastAPI", "react": "React",
            "django": "Django", "flask": "Flask", "postgresql": "PostgreSQL", "mysql": "MySQL",
            "mongodb": "MongoDB", "redis": "Redis", "qdrant": "Qdrant", "rag": "RAG",
            "hybrid search": "Hybrid Search", "docker": "Docker", "aws": "AWS", "gcp": "GCP",
            "data structures": "Data Structures", "algorithms": "Algorithms", "system design": "System Design",
            "dbms": "DBMS", "indexing": "Indexing", "machine learning": "Machine Learning"
        }
        
        detected_skills = sorted(list(set(name for kw, name in all_skills_map.items() if kw in text_lower)))
        if not detected_skills:
            detected_skills = ["Python", "FastAPI", "PostgreSQL", "RAG", "Algorithms"]

        projects = []
        if "rag" in text_lower or "qdrant" in text_lower or "enterprise" in text_lower:
            projects.append(ProjectTechDetail(
                name="Enterprise RAG System",
                technologies=["FastAPI", "Qdrant", "PostgreSQL", "BM25"],
                topics=["RAG", "FastAPI", "Qdrant", "Hybrid Search", "Vector Search"]
            ))
            
        projects.append(ProjectTechDetail(
            name="Full-Stack Technical Application",
            technologies=[s for s in detected_skills[:4]],
            topics=[s for s in detected_skills[:5]]
        ))

        compact_summary = f"Candidate proficient in {', '.join(detected_skills[:6])}. Key projects include {', '.join([p.name for p in projects])}."

        return ResumeDataSchema(
            skills=detected_skills,
            languages=[s for s in detected_skills if s in ["Python", "Java", "C++", "JavaScript", "TypeScript", "SQL"]],
            frameworks=[s for s in detected_skills if s in ["FastAPI", "React", "Django", "Flask"]],
            databases=[s for s in detected_skills if s in ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Qdrant", "DBMS"]],
            cloud=[s for s in detected_skills if s in ["GCP", "AWS", "Docker"]],
            projects=projects,
            experience=["Software Engineering Project Experience"],
            certifications=[],
            compact_context=compact_summary
        )
