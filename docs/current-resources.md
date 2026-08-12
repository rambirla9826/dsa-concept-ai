# Current Resources Audit & Reuse Matrix

| Resource | Current Purpose | Current Location | Can It Be Reused? | What Needs To Change? |
|---|---|---|---|---|
| **Frontend Framework** | React 18 + Vite + TS SPA | `/frontend` | **REUSE 100%** | Add Voice Interview UI, Resume Upload Modal, Audio Visualization state, and Interview Report views. |
| **Styling & UI Tokens** | Tailwind CSS + Glassmorphism system | `/frontend/src/index.css` | **REUSE 100%** | Add pulse glow, listening indicator, and voice mic wave animations. |
| **Backend Framework** | Python FastAPI Web Server | `/backend/main.py` | **REUSE 100%** | Register new `/api/v1/interviews` and `/api/v1/resumes` route handlers. |
| **Database Engine** | Cloud Firestore / LocalJSONDB | `/backend/app/core/db.py` | **REUSE 100%** | Add collections: `resumes`, `interviews`, `interview_questions`, `interview_evaluations`, `interview_limits`, `interview_config`, `audit_logs`. |
| **Authentication & RBAC** | JWT Auth + Role verification | `/backend/app/core/security.py` | **REUSE 100%** | Protect interview APIs; enforce atomic student interview limit checks. |
| **AI Evaluation Engine** | Gemini 1.5 Flash structured evaluator | `/backend/app/services/gemini_evaluator.py` | **REUSE & EXTEND** | Add `resume_analyzer.py` for structured skill extraction and `interview_engine.py` for adaptive question synthesis. |
| **Deterministic Scoring** | Bounded 0-100 weighted math | `/backend/app/services/scoring_engine.py` | **REUSE & EXTEND** | Add interview dimension weighting (Technical Correctness 40%, Concept Understanding 25%, Reasoning 15%, Completeness 10%, Practical 10%). |
| **Student Dashboard** | Progress metrics & recommendations | `/frontend/src/pages/student/StudentDashboard.tsx` | **REUSE & EXTEND** | Add "AI Technical Interview" attempt tracker card (`Used / Allowed`), best score badge, and "Start Interview" button. |
| **Admin Dashboard** | Control panel & user management | `/frontend/src/pages/admin/AdminDashboard.tsx` | **REUSE & EXTEND** | Add Admin Interview Limit Manager, Rubric Weight Adjuster, User Attempt Reset button, and Interview Analytics. |
| **Voice Processing** | Speech-to-Text & Text-to-Speech | Browser Web Speech API + Backend Abstraction | **NEW (FREE)** | Add `speech_service.py` with `SpeechToTextService` and `TextToSpeechService` interfaces using zero-cost browser native APIs. |
