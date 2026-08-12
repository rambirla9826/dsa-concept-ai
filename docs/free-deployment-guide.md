# Free Deployment Guide — AlgoConcept AI

This document provides step-by-step instructions to deploy your complete **AlgoConcept AI** platform (Frontend + FastAPI Backend + Database + AI Voice Technical Interview) on **100% FREE cloud resources**.

---

## 🎯 Architecture & Free Hostings Used

| Component | Free Platform | Free Plan Limits | Cost |
|---|---|---|---|
| **Backend API** | [Render.com](https://render.com) or [Koyeb](https://koyeb.com) | 750 free web service hours/month | **$0.00 / Free** |
| **Frontend Web App** | [Vercel](https://vercel.com) or [Netlify](https://netlify.com) | 100 GB bandwidth / unlimited builds | **$0.00 / Free** |
| **Database** | Built-in Firestore / LocalJSONDB | 1GB storage / 50k reads daily | **$0.00 / Free** |
| **AI Model** | Google Gemini 1.5 Flash API | 15 RPM / 1M TPM / 1,500 evals/day | **$0.00 / Free** |
| **Speech STT/TTS** | Browser Native Web Speech API | Unlimited native browser execution | **$0.00 / Free** |

---

## STEP 1: Deploy Backend API to Render (100% Free)

1. **Sign Up / Log In to Render**:
   - Go to [render.com](https://render.com) and log in with GitHub or email.

2. **Create New Web Service**:
   - Click **New +** → **Web Service**.
   - Connect your GitHub repository (or choose **Deploy from Git repo**).
   - Select the `backend/` directory.

3. **Configure Free Service**:
   - **Name**: `algoconcept-backend`
   - **Environment**: `Python 3`
   - **Region**: Select closest region (e.g. Oregon / Frankfurt / Singapore)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Select **Free** ($0/month).

4. **Environment Variables**:
   Under **Environment Variables**, add:
   - `JWT_SECRET`: `super_secret_jwt_key_algoconcept_2026`
   - `GEMINI_API_KEY`: *(Your Google AI Studio Gemini API Key)*

5. **Deploy**:
   - Click **Create Web Service**.
   - Render will build and deploy your backend.
   - Copy your public backend URL (e.g. `https://algoconcept-backend.onrender.com`).

---

## STEP 2: Deploy Frontend Web App to Vercel (100% Free)

1. **Sign Up / Log In to Vercel**:
   - Go to [vercel.com](https://vercel.com) and log in with GitHub.

2. **Import Project**:
   - Click **Add New...** → **Project**.
   - Select your repository.
   - Set **Root Directory** to `frontend`.

3. **Configure Build Settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Environment Variables**:
   Add variable (if connecting to remote backend URL):
   - `VITE_API_BASE_URL`: `https://algoconcept-backend.onrender.com/api/v1`

5. **Deploy**:
   - Click **Deploy**.
   - Vercel will build your static SPA in ~20 seconds.
   - You will get a live production URL (e.g., `https://algoconcept-ai.vercel.app`).

---

## STEP 3: Verify Live Deployment

1. Open your live Vercel URL in your browser.
2. Sign in as Master Admin (`admin@algoconcept.ai` / `AdminPass123!`).
3. Test uploading a PDF resume, launching an AI Voice Technical Interview, listening to AI spoken questions, and viewing your topic-wise report card.
4. Open the Admin Portal to view user interview limits, grant attempts, or adjust rubric weights.

---

## 🔒 Zero Billing Guarantee
All services above operate strictly within non-expiring free tiers. No credit card activation is required.
