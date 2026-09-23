"""Anti-spoofing liveness detection (the project's flagship feature).

Two complementary passive checks run against frames captured by the webcam:

1. Blink detection — eye aspect ratio (EAR) over a frame sequence. A real
   person blinks; a printed photo or a replayed screen never does.
2. Head-pose challenge — the server issues a random direction (left/right/up);
   yaw/pitch estimated from 68 landmarks must move in the challenged direction.
   A photo cannot respond; a replayed video cannot know the challenge.

Both use the same 68-point landmark model already loaded by the face pipeline,
so the runtime cost is one shape prediction per frame.
"""

import numpy as np

from app.ml.face import _get_models

# Eye aspect ratio (EAR) constants
EAR_BLINK_THRESHOLD = 0.20  # eye considered closed below this ratio
EAR_MIN_BLINKS = 1

# Head pose angles (degrees). Landmark indices refer to the 68-point model.
NOSE_TIP, CHIN, LEFT_EYE, RIGHT_EYE = 30, 8, 36, 45
_LEFT_FACE, _RIGHT_FACE = 0, 16
YAW_TURN_THRESHOLD = 8.0  # degrees of yaw change needed to accept a turn
PITCH_NOD_THRESHOLD = 8.0

# Challenge types
CHALLENGE_LEFT = "turn_left"
CHALLENGE_RIGHT = "turn_right"
CHALLENGE_UP = "look_up"

CHALLENGES = [CHALLENGE_LEFT, CHALLENGE_RIGHT, CHALLENGE_UP]


def estimate_head_pose(landmarks) -> tuple[float, float]:
    """
    Coarse yaw/pitch from 2D landmark geometry (degrees).

    Yaw: horizontal offset of the nose tip from the midpoint between the
    face boundary extremes, normalized by face width.
    Pitch: vertical offset of the nose tip from the eye-mouth midpoint,
    normalized by face height.
    """
    points = np.array([[p.x, p.y] for p in landmarks.parts()], dtype=float)

    face_width = points[_RIGHT_FACE, 0] - points[_LEFT_FACE, 0]
    face_mid_x = (points[_LEFT_FACE, 0] + points[_RIGHT_FACE, 0]) / 2
    yaw_ratio = (points[NOSE_TIP, 0] - face_mid_x) / face_width

    eye_mid_y = (points[LEFT_EYE, 1] + points[RIGHT_EYE, 1]) / 2
    face_height = points[CHIN, 1] - eye_mid_y
    pitch_ratio = (points[NOSE_TIP, 1] - (eye_mid_y + points[CHIN, 1]) / 2) / face_height

    # Convert ratios to approximate degrees (empirically calibrated range).
    yaw = yaw_ratio * 180.0
    pitch = pitch_ratio * 120.0
    return float(yaw), float(pitch)


def eye_aspect_ratio(landmarks, side: str) -> float:
    """EAR for 'left' or 'right' eye from the 68-point layout."""
    idx = range(36, 42) if side == "left" else range(42, 48)
    points = np.array([[landmarks.parts()[i].x, landmarks.parts()[i].y] for i in idx], dtype=float)

    # EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    v1 = np.linalg.norm(points[1] - points[5])
    v2 = np.linalg.norm(points[2] - points[4])
    h = np.linalg.norm(points[0] - points[3])
    return float((v1 + v2) / (2.0 * h)) if h else 0.0


def analyze_liveness(frames: list[np.ndarray], challenge: str) -> dict:
    """
    Run blink + challenge verification over a frame sequence.

    Returns {passed, blink_detected, pose_verified, max_ear_delta, yaw_delta, reason}.
    """
    detector, sp, _ = _get_models()

    ears: list[float] = []
    poses: list[tuple[float, float]] = []
    face_found = False

    for frame in frames:
        rects = detector(frame, 1)
        if not rects:
            continue
        face_found = True

        rect = max(rects, key=lambda r: r.width() * r.height())
        shape = sp(frame, rect)
        ears.append((eye_aspect_ratio(shape, "left") + eye_aspect_ratio(shape, "right")) / 2)
        poses.append(estimate_head_pose(shape))

    result = {
        "passed": False,
        "face_found": face_found,
        "blink_detected": False,
        "pose_verified": False,
        "max_ear_delta": 0.0,
        "yaw_delta": 0.0,
        "reason": "",
    }

    if not face_found:
        result["reason"] = "No face found in the captured frames"
        return result

    # --- Blink check -------------------------------------------------------
    if ears:
        result["max_ear_delta"] = float(max(ears) - min(ears))
        closed_samples = sum(1 for e in ears if e < EAR_BLINK_THRESHOLD)
        result["blink_detected"] = closed_samples >= 1 and result["max_ear_delta"] >= 0.06

    # --- Challenge check ---------------------------------------------------
    if poses:
        yaw_start, yaw_end = poses[0][0], poses[-1][0]
        pitch_start, pitch_end = poses[0][1], poses[-1][1]
        result["yaw_delta"] = float(yaw_end - yaw_start)

        if challenge == CHALLENGE_LEFT:
            result["pose_verified"] = result["yaw_delta"] <= -YAW_TURN_THRESHOLD
        elif challenge == CHALLENGE_RIGHT:
            result["pose_verified"] = result["yaw_delta"] >= YAW_TURN_THRESHOLD
        elif challenge == CHALLENGE_UP:
            result["pose_verified"] = (pitch_end - pitch_start) <= -PITCH_NOD_THRESHOLD

    # --- Decision ----------------------------------------------------------
    blink_ok = result["blink_detected"]
    pose_ok = result["pose_verified"]

    if blink_ok and pose_ok:
        result["passed"] = True
        result["reason"] = "Liveness confirmed"
    elif blink_ok and not pose_ok:
        result["reason"] = "Blink seen but head did not follow the challenge"
    elif pose_ok and not blink_ok:
        result["reason"] = "Head moved but no blink detected"
    else:
        result["reason"] = "No blink and no challenge response — likely a static image"

    return result
