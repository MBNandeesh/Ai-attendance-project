# Architecture

## System overview

```
┌─────────────────────────────┐          ┌──────────────────────────────────┐
│  Next.js 16 (Vercel)        │   HTTPS  │  FastAPI (Render)                │
│                             │─────────►│                                  │
│  /            landing       │          │  /api/v1/auth/teacher   JWT      │
│  /login       teacher auth  │          │  /api/v1/auth/student   JWT      │
│  /student     face login +  │          │  /api/v1/students       face ML  │
│               dashboard     │          │  /api/v1/subjects       CRUD     │
│  /dashboard   teacher       │          │  /api/v1/join/{code}    enroll   │
│               workspace     │          │  /api/v1/attendance     sessions │
│                             │          │  /api/v1/liveness       🏆       │
│  getUserMedia() webcam      │          │  /api/v1/voice          voice ML │
│  MediaRecorder audio        │          │                                  │
└─────────────────────────────┘          └───────────────┬──────────────────┘
                                                         │ SQLAlchemy
                                          ┌──────────────▼──────────────┐
                                          │  SQLite (dev) / Neon (prod) │
                                          └─────────────────────────────┘
```

## ML pipelines

### Face recognition
1. **Detect** — dlib HOG detector, three passes (2× upsample, 3× fallback, horizontally-flipped frame), merged by IoU ≥ 0.5, filtered by minimum face size.
2. **Embed** — 68-point shape predictor → metric-learning descriptor (128-D) with 3 jitter resamples.
3. **Match** — vectorized L2 distances against all enrolled samples; accept only if best distance ≤ 0.55 **and** margin over second-best candidate ≥ 0.10 (ambiguity rejection).

### Liveness detection (flagship)
1. Server issues a **random, single-use challenge** (`turn_left` / `turn_right` / `look_up`) bound to a 120-second session token.
2. Client captures ~30 frames across the challenge.
3. **Blink check** — eye aspect ratio (EAR) over the sequence; a genuine blink dips below 0.20 with ≥ 0.06 delta.
4. **Head-pose check** — coarse yaw/pitch from landmark geometry; the challenged direction must show ≥ 8° movement.
5. Both checks must pass. A printed photo cannot blink or respond; a replayed video cannot know the challenge.

### Voice verification
Resemblyzer (256-D GE2E speaker embeddings) → voice-activity segmentation of classroom audio → per-segment cosine-similarity identification against enrolled profiles (threshold 0.65).

## Data model

```
teachers ──┐
           ├─< subjects >── subject_students >── students
           │        │                             │
           │        └─< attendance_sessions       │
           │                 │                    │
           └─< attendance_corrections >── attendance_logs >──┘
```

- `attendance_sessions` gives every class meeting a first-class identity (fixes the v1 timestamp-string hack).
- Unique constraint `(student_id, session_id)` makes re-submission idempotent.
- `liveness_score` is stored per log for the evaluation chapter.
- `attendance_corrections` provides an audit trail for manual overrides.

## Security decisions

| Decision | Rationale |
|---|---|
| JWT access (24h) + refresh (14d) | stateless horizontal scaling; short blast radius |
| Role claim enforced per-route | a student token cannot reach teacher endpoints (tested) |
| DB access only from backend | no anon-key exposure (v1's Supabase weakness eliminated) |
| Single-use liveness tokens | prevents replaying a captured challenge response |
| Duplicate-face guard at 0.40 distance | one human = one profile |
