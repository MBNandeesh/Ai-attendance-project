# AI Attendance System — End-to-End Project Plan

> **Goal:** Transform the existing Streamlit prototype into a production-grade full-stack web application (Next.js + FastAPI) suitable as a college major project and a CV headline.
>
> **Timeline:** ~8 weeks · **Flagship feature:** Anti-spoofing liveness detection

---

## 1. Current State (What Exists Today)

The repo currently contains a working Streamlit prototype (`ai-attendance-project-app/`):

| Layer | Status | Details |
|---|---|---|
| Face recognition | ✅ Working | dlib HOG detector + 128-D descriptors, multi-angle detection, duplicate-face guard, margin-based matching |
| Voice recognition | ✅ Working | Resemblyzer speaker embeddings, bulk classroom audio segmentation |
| Teacher portal | ✅ Working | Register/login (bcrypt), subjects, QR join codes, photo + voice attendance, records table |
| Student portal | ✅ Working | Face ID login (passwordless), face sample management, enrollment, attendance stats |
| Database | ✅ Working | Supabase Postgres: `teachers`, `students`, `subjects`, `subject_students`, `attendance_logs` |
| Tests | ❌ None | Zero test files in the entire repo |
| Deployment | ❌ None | Local only |
| Docs | ❌ Minimal | README is one line |
| Evaluation | ❌ None | No accuracy / FAR / FRR metrics |
| Anti-spoofing | ❌ None | A printed photo can mark a student present |
| Dead code | ⚠️ Present | `teacher_command_center*.py`, `teacher_dashboard_ui.py` (monkey-patched out), ~11 overlapping CSS files |

### Key decisions locked in
- **Architecture:** Migrate to full-stack web — **Next.js (frontend) + FastAPI (backend)**
- **Flagship:** Anti-spoofing liveness detection
- **Timeline:** 1–2 months (planned as 8 weeks)

---

## 2. Target Architecture

```
┌──────────────────────────────┐         ┌──────────────────────────────┐
│  Frontend — Next.js 14+      │  REST   │  Backend — FastAPI (Python)  │
│  (Vercel deploy)             │◄───────►│  (Render/Railway deploy)     │
│                              │         │                              │
│  • Teacher dashboard         │         │  • Auth (JWT access+refresh) │
│  • Student portal            │         │  • Face pipeline (dlib)      │
│  • Live webcam capture       │         │  • Voice pipeline (Resemblyzer)│
│  • MediaRecorder voice       │         │  • Liveness detector (NEW)   │
│  • Charts (Recharts)         │         │  • Report generation (PDF)   │
│  • Tailwind + shadcn/ui      │         │  • Supabase (Postgres + RLS) │
└──────────────────────────────┘         └──────────────────────────────┘
                                                    │
                                         ┌──────────▼──────────┐
                                         │  Supabase Postgres  │
                                         │  + RLS policies     │
                                         │  + Storage (photos) │
                                         └─────────────────────┘
```

**Why this split wins on a CV:** the ML inference lives in a proper Python service with typed endpoints and tests, the frontend is a modern React/Next.js SPA — recruiters see "designed and deployed a full-stack ML system," not "built a Streamlit script."

### Tech stack
| Concern | Choice |
|---|---|
| Frontend | Next.js 14+ (App Router), TypeScript, Tailwind CSS, shadcn/ui, Recharts |
| Backend | FastAPI, Pydantic v2, Uvicorn |
| Auth | JWT access/refresh tokens (teacher: username+password bcrypt; student: face login + JWT) |
| Database | Supabase Postgres (reuse existing tables) + Row Level Security |
| ML — face | Keep dlib + face_recognition_models (proven in the prototype) |
| ML — voice | Keep Resemblyzer + librosa |
| ML — liveness | Eye-blink + head-pose liveness (see §4) |
| Reports | ReportLab or WeasyPrint (PDF), CSV export |
| Testing | pytest + httpx (backend), Playwright (frontend e2e), GitHub Actions CI |
| Deploy | Vercel (frontend) + Render/Railway Docker (backend) |

---

## 3. Database Schema (migration + additions)

Keep existing tables; add these:

```sql
-- Session-based attendance dedup + liveness evidence
ALTER TABLE attendance_logs
  ADD COLUMN IF NOT EXISTS session_id uuid,
  ADD COLUMN IF NOT EXISTS method text CHECK (method IN ('face','voice','manual')),
  ADD COLUMN IF NOT EXISTS liveness_score float;

CREATE TABLE IF NOT EXISTS attendance_sessions (
  session_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id   bigint REFERENCES subjects(subject_id),
  teacher_id   bigint REFERENCES teachers(teacher_id),
  started_at   timestamptz DEFAULT now(),
  ended_at     timestamptz,
  method       text NOT NULL
);

-- Teacher note on manual overrides (audit trail)
CREATE TABLE IF NOT EXISTS attendance_corrections (
  correction_id bigserial PRIMARY KEY,
  attendance_id bigint REFERENCES attendance_logs,
  teacher_id    bigint REFERENCES teachers(teacher_id),
  old_value     boolean,
  new_value     boolean,
  reason        text,
  created_at    timestamptz DEFAULT now()
);
```

**Security must-do:** enable Row Level Security so the anon key cannot read embeddings. The FastAPI backend uses the service key server-side; the frontend never touches Supabase directly.

---

## 4. Flagship: Anti-Spoofing Liveness Detection

**Problem it solves:** someone holds up a classmate's photo → today the system marks them present.

**Approach (passive liveness, works with the webcam the student already has):**

1. **Blink detection** — dlib facial landmarks (68-point, already loaded) → eye aspect ratio (EAR). Student watches a 3-second prompt; server verifies ≥1 blink detected across sampled frames. Printed photos and screens can't blink.
2. **Head-pose challenge** — PnP head-pose estimation from landmarks. Random instruction: "turn left / turn right / look up." Screens replay attacks fail because the server issues a random challenge per session.
3. **Texture analysis (stretch goal)** — patch-based LBP or a small CNN classifier (real vs. screen/replay). Even a modest accuracy boost here is a great report chapter.

**Flow:** frontend captures 30–60 frames via webcam → POST to `/api/v1/liveness/verify` with the session challenge → backend runs blink + pose checks → returns `liveness_score` → only then is the face-embedding compared for recognition.

**Report chapter this enables:** "Passive Liveness for Face-Based Attendance: Blink Dynamics and Challenge-Response Head Pose" — with FAR/FRR before vs. after liveness.

---

## 5. API Design (FastAPI)

```
POST /api/v1/auth/teacher/register
POST /api/v1/auth/teacher/login          → JWT pair
POST /api/v1/auth/student/face-login     → multipart frames → JWT pair
POST /api/v1/students/register           → face(+voice) enrollment
POST /api/v1/students/{id}/face-samples

GET    /api/v1/subjects                  (teacher's subjects)
POST   /api/v1/subjects
POST   /api/v1/subjects/{id}/join-code   → QR payload
POST   /api/v1/subjects/{id}/enroll      (student or join-code)

POST   /api/v1/liveness/challenge        → random challenge for session
POST   /api/v1/liveness/verify           → frames → liveness_score
POST   /api/v1/attendance/face           → images + liveness proof → attendance
POST   /api/v1/attendance/voice          → audio → attendance
GET    /api/v1/attendance/session/{id}
GET    /api/v1/attendance/records?subject_id=&from=&to=
PATCH  /api/v1/attendance/{id}           → manual override (audited)

GET    /api/v1/analytics/subject/{id}    → trends, defaulters
GET    /api/v1/reports/subject/{id}.pdf
GET    /api/v1/reports/subject/{id}.csv
```

---

## 6. Project Structure (after migration)

```
ai-attendance-system/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app factory, CORS, routers
│   │   ├── core/config.py          # pydantic-settings, secrets from env
│   │   ├── core/security.py        # JWT, bcrypt
│   │   ├── api/v1/                 # routers (auth, attendance, ...)
│   │   ├── ml/
│   │   │   ├── face.py             # ported face pipeline
│   │   │   ├── voice.py            # ported voice pipeline
│   │   │   └── liveness.py         # NEW flagship
│   │   ├── db/                     # supabase client + queries
│   │   └── schemas/                # pydantic request/response models
│   ├── tests/                      # pytest + httpx (unit + API tests)
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── app/                        # Next.js App Router
│   │   ├── (teacher)/dashboard/...
│   │   ├── (student)/portal/...
│   │   └── login/...
│   ├── components/                 # shadcn/ui + custom
│   ├── lib/api.ts                  # typed API client
│   └── tests/                      # Playwright e2e
├── .github/workflows/ci.yml        # lint + typecheck + tests on every push
├── docs/
│   ├── architecture.md             # diagrams for the report
│   ├── evaluation.md               # FAR/FRR/liveness experiments
│   └── report/                     # final college report + viva prep
└── README.md
```

The old Streamlit app stays in the repo as `legacy/` (nice story: "v1 prototype → v2 production").

---

## 7. 8-Week Roadmap

### Week 1 — Foundation & cleanup
- [ ] Scaffold `backend/` (FastAPI + pydantic-settings) and `frontend/` (Next.js + TS + Tailwind)
- [ ] Port DB layer to backend; keep Streamlit app untouched as legacy
- [ ] Set up GitHub Actions CI (ruff, mypy, pytest, next build) — from day 1
- [ ] Enable RLS in Supabase; move all DB access server-side
- [ ] JWT auth: teacher register/login, protected routes

### Week 2 — Auth + student flows
- [ ] Face-login endpoint (port `face_pipeline.py` logic into `ml/face.py`)
- [ ] Student registration with duplicate-face guard
- [ ] Face-sample management
- [ ] Next.js student portal UI (login → dashboard → subjects)

### Week 3 — Teacher flows
- [ ] Subjects CRUD, join codes + QR
- [ ] Enrollment (individual + join-code auto-enroll)
- [ ] Photo attendance upload → recognition → review → confirm (audited)

### Week 4 — Voice attendance + sessions
- [ ] Port voice pipeline; MediaRecorder capture in frontend
- [ ] Attendance sessions table + dedup (replaces timestamp-string hack)
- [ ] Attendance records with filters (subject/date range)

### Week 5 — 🏆 Liveness detection (flagship)
- [ ] Frontend webcam frame capture + challenge UX ("turn your head left…")
- [ ] EAR blink detection + PnP head-pose verification in `ml/liveness.py`
- [ ] Wire into face attendance; store `liveness_score`
- [ ] Unit tests with synthetic landmark sequences

### Week 6 — Analytics, reports, polish
- [ ] Analytics: per-subject trends, defaulters list (Recharts)
- [ ] PDF + CSV report exports
- [ ] Manual override with audit trail
- [ ] Responsive/mobile pass

### Week 7 — Evaluation & hardening
- [ ] **Evaluation experiments** (big CV/report value):
  - Face recognition accuracy vs. distance/lighting
  - FAR/FRR with and without liveness (spoof attack attempts)
  - Voice identification accuracy in noisy classroom audio
- [ ] Rate limiting, error handling, logging
- [ ] Load-test the recognition endpoint (it should batch, not per-student loop)
- [ ] Write `docs/evaluation.md`

### Week 8 — Deploy & document
- [ ] Backend: Dockerfile → Render/Railway; Frontend: Vercel
- [ ] Landing page, demo credentials, seed script for demo data
- [ ] Rewrite README: hero screenshot, architecture diagram, live demo link, metrics table
- [ ] Final report + viva materials (problem statement, literature, architecture, evaluation, screenshots, future work)

---

## 8. CV Positioning (what to write when it's done)

> **AI Attendance System** — Full-stack ML web app (Next.js · FastAPI · Supabase)
> - Built a passwordless attendance platform using dlib face embeddings and Resemblyzer speaker verification, deployed end-to-end on Vercel + Render.
> - Designed a challenge-response liveness detector (blink dynamics via eye-aspect-ratio + head-pose estimation) that reduced photo-spoof acceptance from 100% to <X%.
> - Evaluated recognition at FAR/FRR across lighting and distance; published metrics in project report.
> - CI (GitHub Actions), 80%+ backend test coverage, JWT auth, Row-Level Security.

Fill in real numbers from Week 7 — quantified results are what make it stand out.

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| dlib build pain on the backend host | Use `dlib-bin` wheels; Docker with python:3.11-slim + cmake layer pinned early (Week 1 spike) |
| Liveness false-rejects annoying real students | Tunable thresholds; liveness score stored but configurable "strict mode" |
| Recognition is O(students) per face | Cache embeddings in memory with TTL; switch to numpy matrix ops (vectorized distances) |
| Free-tier host kills model container (RAM) | Keep models ~100MB; use Render free tier + cold-start warmup endpoint, or Hugging Face Spaces for the ML service |
| Scope creep | Anything not in the roadmap goes to a "future work" slide, not the codebase |
