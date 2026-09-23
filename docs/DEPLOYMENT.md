# Deployment Guide — Live in 15 Minutes

Free-tier deployment: **Neon Postgres** (DB) + **Render** (API) + **Vercel** (frontend).

> Deploy order matters: Database → Backend (get its URL) → Frontend (point at backend URL).

---

## 1. Database — Neon (free, no expiry)

1. Sign up at [neon.tech](https://neon.tech) with GitHub.
2. Create project → name it `ai-attendance`.
3. Copy the **connection string** (looks like `postgresql://user:pass@ep-xxx.aws.neon.tech/neondb?sslmode=require`).
4. Save it — this is your `DATABASE_URL`. Tables create automatically on first backend startup.

---

## 2. Backend — Render (free web service)

**Easiest — Blueprint (auto-detects `render.yaml`):**

1. Push this repo to GitHub (done).
2. [render.com](https://render.com) → **New +** → **Blueprint** → select `MBNandeesh/Ai-attendance-project`.
3. Render reads `render.yaml` and creates the `ai-attendance-api` service.
4. When prompted, fill the two `sync: false` variables:
   - `DATABASE_URL` → your Neon connection string, **but change the prefix** to `postgresql+psycopg://` (SQLAlchemy driver).
   - `CORS_ORIGINS` → your future Vercel URL (step 3). You can add it after deploying the frontend (Render lets you edit env vars anytime; the service redeploys automatically).

**Manual alternative:** New + → Web Service → repo → Root Directory `backend` → Build `pip install -e ".[ml]"` → Start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

5. Wait for the build (~5 min; dlib compiles in Render's free tier).
6. Verify: open `https://<your-service>.onrender.com/api/health` → `{"status":"ok","environment":"production"}`.
7. Note your API base URL: `https://<your-service>.onrender.com`.

> ⚠️ **Free-tier cold starts:** the service sleeps after 15 min idle; first request takes ~50s to wake. For your demo/viva, ping the health endpoint a minute before presenting.

---

## 3. Frontend — Vercel

1. [vercel.com](https://vercel.com) → **Add New Project** → Import `MBNandeesh/Ai-attendance-project`.
2. **Root Directory:** `frontend`
3. Environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://<your-service>.onrender.com` (no trailing slash)
4. Deploy → get your URL: `https://ai-attendance.vercel.app` (or similar).
5. Go back to Render → your service → Environment → edit `CORS_ORIGINS` → set it to exactly that Vercel URL (with `https://`, no trailing slash) → Save (auto-redeploys).

---

## 4. Verify the live system

| Check | How |
|---|---|
| API up | `curl https://<api>.onrender.com/api/health` |
| DB connected | `curl https://<api>.onrender.com/api/health/db` |
| Frontend loads | Open the Vercel URL — landing page renders |
| Face registration | Student portal → allow camera → register a face → dashboard appears |
| End-to-end | Teacher: register → create subject → copy join code. Student: face-register → join by code. Teacher: take attendance → student marked present |

---

## Local development (already working)

```bash
# Terminal 1
cd backend && pip install -e ".[dev,ml]" && uvicorn app.main:app --port 8000

# Terminal 2
cd frontend && npm install && npm run dev
```

Open any port Next prints (3000, or 58579 etc.) — the backend now accepts **any localhost origin** in development, so camera login and registration work regardless of which port the dev server picks.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Browser console: CORS blocked | `CORS_ORIGINS` missing the Vercel URL | Add exact origin (scheme + host, no slash) in Render env |
| "ML dependencies are not installed" (503) | backend deployed without `[ml]` extras | Build command must be `pip install -e ".[ml]"` |
| First request very slow | Render free cold start | Normal; ping `/api/health` first |
| Camera denied | Browser needs HTTPS or localhost | Vercel (HTTPS) works; never mixed-content |
| Face not recognized but registered | Strict margin threshold | Add more face samples (student dashboard) |
