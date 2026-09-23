"""Liveness logic tests. analyze_liveness is exercised with monkeypatched
dlib detection so tests are fast and deterministic; the real dlib path is
covered by the integration suite."""

import numpy as np

from app.ml.liveness import analyze_liveness, estimate_head_pose, eye_aspect_ratio
from app.services.challenge_store import issue_challenge, pop_challenge


class FakePart:
    def __init__(self, x, y):
        self.x, self.y = x, y


class FakeLandmarks:
    def __init__(self, parts):
        self._parts = parts

    def parts(self):
        return self._parts


def _neutral_landmarks() -> FakeLandmarks:
    """68-point layout with eyes open, facing forward."""
    pts = []
    # Jaw 0-16: horizontal line
    for i in range(17):
        pts.append(FakePart(30 + i * 10, 120))
    # Brows 17-26
    for i in range(10):
        pts.append(FakePart(50 + i * 10, 70))
    # Nose 27-35; tip (index 30) sits at the eye-chin midpoint (y=105)
    for i in range(9):
        pts.append(FakePart(110, 90 + i * 5))
    # Left eye 36-41 (open: tall)
    lx, ly = 70, 90
    pts += [FakePart(lx, ly), FakePart(lx + 4, ly - 5), FakePart(lx + 8, ly - 5),
            FakePart(lx + 12, ly), FakePart(lx + 8, ly + 5), FakePart(lx + 4, ly + 5)]
    # Right eye 42-47 (open)
    rx, ry = 130, 90
    pts += [FakePart(rx, ry), FakePart(rx + 4, ry - 5), FakePart(rx + 8, ry - 5),
            FakePart(rx + 12, ry), FakePart(rx + 8, ry + 5), FakePart(rx + 4, ry + 5)]
    # Mouth 48-67
    for i in range(20):
        pts.append(FakePart(80 + (i % 10) * 6, 110))
    return FakeLandmarks(pts)


def test_ear_open_eye_high():
    assert eye_aspect_ratio(_neutral_landmarks(), "left") > 0.3


def test_pose_neutral_is_centered():
    yaw, pitch = estimate_head_pose(_neutral_landmarks())
    assert abs(yaw) < 5
    assert abs(pitch) < 5


def test_challenge_store_single_use():
    token, challenge, instruction = issue_challenge()
    assert instruction
    assert pop_challenge(token) == challenge
    assert pop_challenge(token) is None  # single use


def test_challenge_store_invalid_token():
    assert pop_challenge("bogus-token") is None


def test_analyze_no_face(monkeypatch):
    import app.ml.liveness as lv

    class EmptyDetector:
        def __call__(self, *a, **k):
            return []

    monkeypatch.setattr(lv, "_get_models", lambda: (EmptyDetector(), None, None))

    frames = [np.zeros((100, 100, 3), dtype=np.uint8)] * 6
    result = analyze_liveness(frames, "turn_left")
    assert result["passed"] is False
    assert "No face" in result["reason"]
