# Resource & Cost Audit (100% Free-First Compliance)

## Executive Guarantee
This document provides a line-item audit of all technologies used for the **AI Voice Technical Interview** system. 

**NO PAID SERVICES ARE REQUIRED.** No credit card activation is necessary. All components strictly operate within Google Free Tiers and browser-native capabilities for 20-30 initial users.

---

## Resource Cost Breakdown Table

| Resource | Already Used | Reused | New | Free Tier Allowance | Potentially Billable? | Purpose in AI Voice Interview |
|---|---|---|---|---|---|---|
| **Google Gemini 1.5 Flash** | Yes | Yes | No | 15 RPM / 1M TPM / 1,500 evals/day | **NO** (Free Tier via AI Studio) | Structured resume skill extraction & adaptive technical question generation |
| **Google Cloud Firestore** | Yes | Yes | No | 50k reads / 20k writes daily / 1GB storage | **NO** (Free Tier) | Storing resumes, interview state, question history, evaluations, limits |
| **FastAPI Backend** | Yes | Yes | No | Local execution / 750 free hrs on Render | **NO** (Free Tier) | Core API, atomic attempt reservation, scoring engine, deduplication |
| **React + Vite Frontend** | Yes | Yes | No | Local execution / Unlimited on Vercel | **NO** (Free Tier) | Two-way voice UI, mic visualization, report cards, admin limits control |
| **Web Speech STT (SpeechRecognition)** | No | No | Yes | Unlimited Browser Native Web Speech API | **NO** ($0 Free Native Browser API) | Real-time speech-to-text conversion of student voice answers |
| **Web Speech TTS (SpeechSynthesis)** | No | No | Yes | Unlimited Browser Native Web Speech API | **NO** ($0 Free Native Browser API) | AI voice question playback in natural speech |
| **PyPDF2 / pdfplumber** | No | No | Yes | Open Source Python Package | **NO** ($0 Free Open Source) | PDF text extraction for resume analysis |
| **Firebase Authentication** | Yes | Yes | No | 50k MAU Free Tier | **NO** (Free Tier) | Secure JWT user identity and RBAC role checks |

---

## 🚫 Explicitly Prohibited Services (Verification)
- **ElevenLabs API**: ❌ Not used (Replaced with 100% Free Web Speech Synthesis / Server Abstraction).
- **Google Cloud Speech-to-Text Paid API**: ❌ Not used (Replaced with 100% Free Browser SpeechRecognition API).
- **OpenAI / Anthropic APIs**: ❌ Not used (Replaced with Google Gemini 1.5 Flash Free Tier).
- **External Paid Vector DB (Pinecone/Qdrant Cloud)**: ❌ Not used (Replaced with lightweight in-memory/backend string semantic deduplication).
- **Paid Redis / Queue Service**: ❌ Not used (Atomic database locks handle 20-30 concurrent users effortlessly).

---

## Cost Assurance Protocol
If any future feature modification requires a billable GCP or third-party service:
1. System will HALT before enabling the service.
2. User will receive an explicit notification outlining:
   - SERVICE NAME
   - REASON REQUIRED
   - FREE ALTERNATIVE
   - POSSIBLE COST
   - EXPECTED USAGE
3. Billing will NEVER be created without explicit user confirmation.
