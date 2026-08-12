# Existing Architecture Documentation

## 1. Executive Overview
This document provides a technical audit of the existing **AlgoConcept AI** application architecture prior to integrating the **AI Voice Technical Interview** system. 

The existing application is a startup-level MVP built for conceptual DSA/algorithm evaluation. It enforces conceptual technical assessment without penalizing non-native English grammar or spelling.

---

## 2. Core Architectural Components

### Frontend Layer
- **Framework**: React 18 + Vite + TypeScript.
- **Styling**: Tailwind CSS + Vanilla CSS custom glassmorphism design system (`index.css`).
- **State & Context**: `AuthContext.tsx` handling JWT token persistence, active user state, and role checks.
- **Icons & Visuals**: `lucide-react`, custom SVG radial gauges (`ScoreGauge.tsx`), difficulty/category badges.
- **Pages**:
  - Student: `StudentDashboard.tsx`, `ProblemList.tsx`, `ProblemView.tsx`, `ResultView.tsx`.
  - Admin: `AdminDashboard.tsx`, `AdminQuestionEditor.tsx`, `AdminUsers.tsx`, `AdminAIUsage.tsx`, `AdminBenchmarks.tsx`.
  - Shared: `Login.tsx`, `Navbar.tsx`.

### Backend Layer
- **Framework**: Python 3.12 + FastAPI + Uvicorn.
- **API Router Structure** (`/api/v1`):
  - `auth.py`: User registration, login, session lookup (`/auth/register`, `/auth/login`, `/auth/me`).
  - `questions.py`: Filterable DSA problem listing, details, progressive hints.
  - `submissions.py`: Natural language answer submission, Gemini AI evaluation invocation, deterministic score logging.
  - `users.py`: Student metrics dashboard data, weak/strong category tracking, recommendations.
  - `admin.py`: Question CRUD, versioning, user management (enable/disable, role promotion/demote, deletion), platform metrics.
  - `ai_usage.py`: Daily quota tracking, error monitoring, rate limits.
  - `benchmarks.py`: Expert human score recording, MAE, agreement rate %, Pearson correlation.

### Database Layer
- **Engine**: Google Cloud Firestore architecture abstracted via `LocalJSONDatabase` (`backend/app/core/db.py`) for zero-setup local execution and seamless GCP Cloud Firestore migration.
- **Collections**:
  - `users`: User profiles, role (`USER` | `ADMIN`), hashed passwords, streak counts, topic performance metrics.
  - `questions`: Problem statements, categories, difficulties, examples, constraints, hints.
  - `question_versions`: Immutable history of published question iterations.
  - `concept_blueprints`: Admin-defined concept items ($C_1..C_n$), weights, mandatory flags, expected complexities.
  - `submissions`: Natural language student responses and evaluation associations.
  - `evaluations`: Granular concept evaluations (`correct`, `partial`, `incorrect`), evidence quotes, dimension scores.
  - `rubrics`: Platform scoring weights (Default: Blueprint 30%, Algo 25%, Reasoning 15%, Time 15%, Space 10%, Edge 5%).
  - `ai_usage`: Audit logs of AI evaluations and rate limit checks.
  - `benchmarks`: Expert human vs AI score comparison records.

### Authentication & Security Layer
- **JWT Authentication**: `pyjwt` tokens signed with `JWT_SECRET`, 24-hour expiration (`security.py`).
- **Password Security**: SHA-256 password hashing with salt.
- **Role-Based Access Control (RBAC)**: `require_admin` FastAPI dependency protecting all `/admin/*` routes. Public signup is strictly locked to `USER` (Student) role.

### AI Evaluation & Deterministic Scoring Engine
- **AI Model**: Google Gemini 1.5 Flash (via `google-genai` / `google-generativeai` SDK with fallback semantic heuristic engine).
- **Prompt Strategy**: Strict system instructions forcing technical evaluation while ignoring English grammar, spelling, or vocabulary style. Enforces structured JSON output schema matching Pydantic model (`GeminiEvaluationSchema`).
- **Deterministic Math Engine** (`scoring_engine.py`):
  - LLM does NOT decide numerical score.
  - Backend calculates score deterministically:
    $$\text{Blueprint Score} = \frac{\sum (w_i \times s_i)}{\sum w_i} \times 100$$
    Weighted across dimensions into a bounded 0-100 final score.

---

## 3. Architecture Extension Strategy for AI Voice Interview

To add the **AI Voice Technical Interview** feature, we WILL NOT create a separate application or replace existing infrastructure. We will **extend** the existing stack:

1. **Frontend**: Add `VoiceInterviewView.tsx`, `InterviewReportView.tsx`, `ResumeUploadModal.tsx`, and `AdminInterviewConfig.tsx` inside existing `src/pages/` and `src/components/`.
2. **Backend**: Add `interviews.py` and `resumes.py` router modules under `backend/app/api/` and `interview_engine.py`, `resume_analyzer.py`, `speech_service.py` under `backend/app/services/`.
3. **Database**: Extend `LocalJSONDatabase` with `resumes`, `interviews`, `interview_questions`, `interview_evaluations`, `interview_limits`, `interview_config` collections.
4. **AI & Speech**: Reuse Gemini 1.5 Flash for resume topic extraction and adaptive question generation. Use **Browser Web Speech API** (SpeechRecognition + SpeechSynthesis) with server-side abstraction interfaces (`SpeechToTextService`, `TextToSpeechService`) for 100% free two-way voice interaction.
