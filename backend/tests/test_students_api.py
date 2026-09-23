"""API tests for student endpoints. The face pipeline is mocked so tests are
fast and deterministic; the pipeline's pure logic is tested in test_face_logic.py,
and a full real-dlib integration test lives in test_face_integration.py."""

import base64
import io
import json

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.db.models import Student
from app.db.session import SessionLocal


@pytest.fixture()
def mock_face(monkeypatch):
    """Replace dlib-backed functions with deterministic fake embeddings."""
    from app.api.v1 import students as students_mod
    from app.ml import store as store_mod

    calls = {"n": 0}

    def fake_embeddings(image_np):
        # Deterministic embedding derived from image brightness so different
        # test images map to different vectors, same image -> same vector.
        value = float(int(image_np.mean()) % 100) / 100
        vec = np.full(128, value)
        calls["n"] += 1
        return [vec]

    monkeypatch.setattr(students_mod.face_pipeline, "get_face_embeddings", fake_embeddings)

    # Real matching logic, but with the fake embedding source.
    def make_known(db):
        return store_mod.load_known_faces(db, force_refresh=True)

    yield calls


def _jpeg_b64(gray_value: int) -> str:
    img = Image.new("RGB", (160, 160), (gray_value, gray_value, gray_value))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()


def _create_student(client: TestClient, name: str, gray_value: int) -> dict:
    resp = client.post(
        "/api/v1/students/register",
        json={"name": name, "face_image": _jpeg_b64(gray_value)},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def _student_headers(client: TestClient, student_id: int) -> dict:
    resp = client.post("/api/v1/auth/student/dev-login", json={"student_id": student_id})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def test_register_student_returns_tokens(client, mock_face):
    data = _create_student(client, "Alice", 10)
    assert data["role"] == "student"
    assert data["access_token"]
    assert data["name"] == "Alice"


def test_register_duplicate_face_conflict(client, mock_face):
    # Distinct gray value so it doesn't collide with students from other tests.
    _create_student(client, "Alice2", 60)
    resp = client.post(
        "/api/v1/students/register",
        json={"name": "Imposter", "face_image": _jpeg_b64(60)},
    )
    assert resp.status_code == 409
    assert "already registered" in resp.json()["detail"]


def test_face_login_success(client, mock_face):
    created = _create_student(client, "Bob", 20)

    resp = client.post("/api/v1/students/face-login", json={"face_image": _jpeg_b64(20)})
    assert resp.status_code == 200
    assert resp.json()["user_id"] == created["user_id"]


def test_face_login_unknown_401(client, mock_face):
    _create_student(client, "Carol", 30)
    resp = client.post("/api/v1/students/face-login", json={"face_image": _jpeg_b64(99)})
    assert resp.status_code == 401


def test_face_login_invalid_image_400(client):
    resp = client.post("/api/v1/students/face-login", json={"face_image": "not-base64!!"})
    assert resp.status_code == 400


def test_add_face_samples(client, mock_face):
    created = _create_student(client, "Dave", 40)
    headers = _student_headers(client, created["user_id"])

    resp = client.post(
        "/api/v1/students/me/face-samples",
        headers=headers,
        json={"face_images": [_jpeg_b64(41), _jpeg_b64(42)]},
    )
    assert resp.status_code == 200

    db = SessionLocal()
    try:
        student = db.get(Student, created["user_id"])
        stored = json.loads(student.face_embedding)
        assert len(stored) == 3  # 1 original + 2 new samples
    finally:
        db.close()


def test_add_samples_requires_auth(client):
    resp = client.post(
        "/api/v1/students/me/face-samples",
        json={"face_images": [_jpeg_b64(1)]},
    )
    assert resp.status_code == 401
