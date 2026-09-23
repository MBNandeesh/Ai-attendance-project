"""Attendance API tests with mocked ML pipelines (real ML logic is unit-tested separately)."""

import base64
import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.db.models import Student, SubjectStudent
from app.db.session import SessionLocal


@pytest.fixture()
def mock_ml(monkeypatch):
    from app.api.v1 import attendance as att

    monkeypatch.setattr(
        att.face_pipeline,
        "identify_faces",
        lambda image, known: [{"student_id": sid, "distance": 0.3} for sid in known],
    )
    monkeypatch.setattr(
        att.voice_pipeline,
        "process_bulk_audio",
        lambda audio, known, threshold=0.65: {sid: 0.8 for sid in known},
    )
    yield


def _jpeg_b64(value: int = 128) -> str:
    img = Image.new("RGB", (160, 160), (value, value, value))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()


def _setup_subject_with_students(client: TestClient, teacher: dict, n: int = 2) -> dict:
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": f"ATT{n}", "name": "Attendance Test"},
    ).json()

    db = SessionLocal()
    try:
        import json

        ids = []
        for i in range(n):
            s = Student(name=f"AttStudent{i}", face_embedding=json.dumps([[0.5] * 128]))
            db.add(s)
            db.flush()
            ids.append(s.student_id)
            db.add(SubjectStudent(student_id=s.student_id, subject_id=subject["subject_id"]))
        db.commit()
    finally:
        db.close()

    return {"subject": subject, "student_ids": ids}


def test_create_session(client, teacher):
    setup = _setup_subject_with_students(client, teacher, 1)
    resp = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    )
    assert resp.status_code == 201
    assert resp.json()["method"] == "face"


def test_face_attendance_marks_everyone_present(client, teacher, mock_ml):
    setup = _setup_subject_with_students(client, teacher, 2)
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    ).json()

    resp = client.post(
        "/api/v1/attendance/face",
        headers=teacher["headers"],
        json={"session_id": session["session_id"], "images": [_jpeg_b64()]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["present_count"] == 2
    assert data["total_students"] == 2


def test_face_attendance_requires_own_session(client, teacher, mock_ml):
    from tests.conftest import create_teacher

    setup = _setup_subject_with_students(client, teacher, 1)
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    ).json()

    other = create_teacher(client)
    resp = client.post(
        "/api/v1/attendance/face",
        headers=other["headers"],
        json={"session_id": session["session_id"], "images": [_jpeg_b64()]},
    )
    assert resp.status_code == 404


def test_voice_attendance_marks_present(client, teacher, mock_ml):
    setup = _setup_subject_with_students(client, teacher, 1)

    # Give the student a fake voice profile.
    db = SessionLocal()
    try:
        import json

        student = db.get(Student, setup["student_ids"][0])
        student.voice_embedding = json.dumps([[0.1] * 256])
        db.commit()
    finally:
        db.close()

    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "voice"},
    ).json()

    resp = client.post(
        "/api/v1/attendance/voice",
        headers=teacher["headers"],
        json={
            "session_id": session["session_id"],
            "audio_base64": base64.b64encode(b"fakeaudiodata").decode(),
        },
    )
    assert resp.status_code == 200
    assert resp.json()["present_count"] == 1


def test_voice_attendance_without_profiles_400(client, teacher, mock_ml):
    setup = _setup_subject_with_students(client, teacher, 1)  # no voice embeddings
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "voice"},
    ).json()

    resp = client.post(
        "/api/v1/attendance/voice",
        headers=teacher["headers"],
        json={
            "session_id": session["session_id"],
            "audio_base64": base64.b64encode(b"fakeaudiodata").decode(),
        },
    )
    assert resp.status_code == 400


def test_session_results_endpoint(client, teacher, mock_ml):
    setup = _setup_subject_with_students(client, teacher, 2)
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    ).json()

    client.post(
        "/api/v1/attendance/face",
        headers=teacher["headers"],
        json={"session_id": session["session_id"], "images": [_jpeg_b64()]},
    )

    resp = client.get(
        f"/api/v1/attendance/sessions/{session['session_id']}",
        headers=teacher["headers"],
    )
    assert resp.status_code == 200
    assert resp.json()["present_count"] == 2


def test_teacher_records_listing(client, teacher, mock_ml):
    setup = _setup_subject_with_students(client, teacher, 1)
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    ).json()

    client.post(
        "/api/v1/attendance/face",
        headers=teacher["headers"],
        json={"session_id": session["session_id"], "images": [_jpeg_b64()]},
    )

    resp = client.get("/api/v1/attendance/records", headers=teacher["headers"])
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_csv_export(client, teacher, mock_ml):
    setup = _setup_subject_with_students(client, teacher, 1)
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    ).json()
    client.post(
        "/api/v1/attendance/face",
        headers=teacher["headers"],
        json={"session_id": session["session_id"], "images": [_jpeg_b64()]},
    )

    resp = client.get("/api/v1/attendance/records/export", headers=teacher["headers"])
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    assert b"Present" in resp.content


def test_student_sees_own_records(client, teacher, mock_ml):
    setup = _setup_subject_with_students(client, teacher, 1)
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    ).json()
    client.post(
        "/api/v1/attendance/face",
        headers=teacher["headers"],
        json={"session_id": session["session_id"], "images": [_jpeg_b64()]},
    )

    sid = setup["student_ids"][0]
    login = client.post("/api/v1/auth/student/dev-login", json={"student_id": sid}).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}

    resp = client.get("/api/v1/attendance/me", headers=headers)
    assert resp.status_code == 200
    records = resp.json()
    assert len(records) == 1
    assert records[0]["is_present"] is True


def test_double_marking_idempotent(client, teacher, mock_ml):
    """Marking the same session twice must not duplicate log rows."""
    setup = _setup_subject_with_students(client, teacher, 2)
    session = client.post(
        "/api/v1/attendance/sessions",
        headers=teacher["headers"],
        json={"subject_id": setup["subject"]["subject_id"], "method": "face"},
    ).json()

    for _ in range(2):
        client.post(
            "/api/v1/attendance/face",
            headers=teacher["headers"],
            json={"session_id": session["session_id"], "images": [_jpeg_b64()]},
        )

    resp = client.get(
        f"/api/v1/attendance/sessions/{session['session_id']}",
        headers=teacher["headers"],
    )
    assert resp.json()["total_students"] == 2  # not 4
