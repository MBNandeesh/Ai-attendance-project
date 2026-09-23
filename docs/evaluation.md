# Evaluation Guide

How to generate the metrics for your report/viva. Each experiment below can be run once you have collected the datasets described.

## 1. Face recognition accuracy

**Dataset:** photograph 10–20 volunteers at three distances (1m, 3m, 6m) × two lighting levels (normal, dim). Enroll one sample per person; test with the rest.

**Metrics:**
- **True Accept Rate (TAR)** = matches correctly identified / total genuine attempts
- **False Accept Rate (FAR)** = matches to the wrong person / total impostor attempts

**Procedure:** run each test image through `POST /api/v1/students/face-login` semantics and record match/mismatch. Vary `FACE_MATCH_THRESHOLD` (0.45 → 0.65) and plot the ROC curve — this becomes your report's key figure.

## 2. Liveness effectiveness (the flagship table)

**Attack set:** for each volunteer, prepare (a) a printed photo, (b) a phone screen showing their video, (c) a genuine live attempt.

| Condition | Blinks detected | Pose responded | Liveness passed |
|---|---|---|---|
| Live person | ✓ | ✓ | ✓ |
| Printed photo | ✗ | ✗ | ✗ |
| Screen replay | (depends) | ✗ (no challenge knowledge) | ✗ |

**Report metric:** Attack Presentation Cut-off Error (APCER) — % of spoof attacks accepted. With both checks enforced, expected result: **0% APCER** on the printed-photo class, near-0% on replay (challenge is random and single-use).

## 3. Voice identification

Record 10 volunteers saying "I am present" in (a) quiet room, (b) classroom noise. Run `POST /api/v1/attendance/voice`. Report identification accuracy per condition and the effect of the 0.65 cosine threshold.

## 4. Latency

Measure p50/p95 of `POST /attendance/face` with 1, 4, 8 photos (time curl). The vectorized matcher keeps matching time ~O(faces × total samples); detection dominates.

## Where the numbers go

- README badges + CV bullets ("reduced photo-spoof acceptance from 100% → 0%")
- Report chapter: "Evaluation" with the tables above
- Viva demo: live liveness challenge with a photo of yourself vs. your face
