# AlgoConcept AI — Conceptual Coding & AI Voice Technical Interview Platform

An end-to-end AI-powered technical evaluation platform and two-way voice technical interview system built with React 18, Vite, FastAPI, Firestore architecture, and Google Gemini 1.5 Flash.

---

## 🌟 Core Features

1. **AI Voice Technical Interview**:
   - **Resume-Aware**: Parses candidate PDF resumes into structured topics & project tech stacks.
   - **Two-Way Voice**: Spoken AI questions via SpeechSynthesis, recorded voice answers via SpeechRecognition.
   - **Deduplication Engine**: Ensures every interview question is unique across all past interviews.
   - **Multi-Interview Memory**: Weak topics from prior interviews feed into future sessions.
   - **Structured Technical Evaluation**: Evaluates technical correctness, reasoning, depth, and completeness without penalizing non-native English grammar or accents.
   - **Targeted Study Recommendations**: 5 granular concept items per weak topic.
2. **Student Attempt Limits**: Backend atomic reservation lock protecting student interview limits.
3. **Admin Portal**: Admin limits manager, attempt reset button, rubric weight configurator, user management, and interview analytics.
4. **100% Free-Tier Compliance**: Uses free-tier Gemini 1.5 Flash + native browser Web Speech API ($0.00 cost).

---

## 🚀 How to Push to GitHub

To upload this repository to your GitHub account:

```bash
# 1. Navigate to project root
cd C:\Users\dell\.gemini\antigravity-ide\scratch\dsa-concept-ai

# 2. Initialize Git
git init
git add .
git commit -m "Initial commit: AlgoConcept AI platform with AI Voice Technical Interview"

# 3. Create a new empty repository on GitHub (github.com/new)
# 4. Link and push to GitHub:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dsa-concept-ai.git
git push -u origin main
```

---

## 🚀 How to Run Locally

### 1. Start Backend API Server (FastAPI)
```bash
cd backend
python main.py
```
- API Server: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

### 2. Start Frontend Server (React + Vite)
```bash
cd frontend
npm run dev
```
- Web Application: `http://localhost:3000`

---

## 🔑 Master Credentials
- **Master Admin Account**: `admin@algoconcept.ai` / `AdminPass123!`
- **Student Accounts**: Register via the Sign Up form on the login page.
