# AI Attendance System

Full-stack, passwordless attendance platform: **Next.js 16** frontend, **FastAPI** backend, dlib face recognition, Resemblyzer voice verification, and **anti-spoofing liveness detection** (blink dynamics + challenge-response head pose).

![status](https://img.shields.io/badge/tests-59%20passing-brightgreen) ![ci](https://img.shields.io/badge/CI-GitHub_Actions-blue)

## Features

- 🧑‍🎓 **Student** — Face ID login (no passwords), self-registration with duplicate-face protection, join subjects by code, per-subject attendance stats, PWA-installable on mobile
- 👩‍🏫 **Teacher** — subject management with unique join codes, photo-based face attendance, bulk voice attendance, session records, CSV export
- 🛡️ **Liveness (flagship)** — webcam challenge ("turn left…") verified via eye-aspect-ratio blink detection + head-pose estimation; printed photos and replayed videos fail
- 🔐 **Security** — JWT access/refresh pairs, role-scoped tokens, bcrypt, server-side-only DB access, auditable manual overrides
- 🏗️ **Engineering** — 59 tests, ruff, GitHub Actions CI, Docker, typed API end-to-end

## Architecture

```
frontend/  Next.js 16 (TS, Tailwind)  →  Vercel
backend/   FastAPI + SQLAlchemy       →  Render (Docker-ready)
             ├── ml/face.py       dlib 128-D embeddings, vectorized matching
             ├── ml/voice.py      Resemblyzer speaker embeddings
             ├── ml/liveness.py   EAR blink + head-pose challenge (flagship)
             └── db/              SQLite (dev) / Neon Postgres (prod)
```

## Run locally

**Backend** (Python 3.11+):

```bash
cd backend
python -m venv venv && venv/Scripts/activate   # or source venv/bin/activate
pip install -e ".[dev,ml]"
uvicorn app.main:app --port 8000
# API docs: http://localhost:8000/api/docs
```

**Frontend** (Node 18+):

```bash
cd frontend
npm install
npm run dev   # http://localhost:3000
```

**Or everything with Docker:**

```bash
docker compose up
```

## Environment

Copy `.env.example` → configure:

| Variable | Where | Purpose |
|---|---|---|
| `JWT_SECRET_KEY` | backend | token signing (32+ chars) |
| `DATABASE_URL` | backend | SQLite by default; Neon Postgres in prod |
| `NEXT_PUBLIC_API_URL` | frontend | backend base URL |

## Testing

```bash
cd backend
pytest tests/          # 59 tests: auth, subjects, enrollment, attendance, liveness, face logic
ruff check .           # lint
```

## Deploy

1. **Database** — create a free Postgres at [neon.tech](https://neon.tech); tables auto-create on startup.
2. **Backend** — Render blueprint (`render.yaml`): set `DATABASE_URL`, JWT secret auto-generated.
3. **Frontend** — `vercel --deploy` from `frontend/`; set `NEXT_PUBLIC_API_URL` to the Render URL.

## Project structure

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the full roadmap and [docs/architecture.md](docs/architecture.md) for system design.
