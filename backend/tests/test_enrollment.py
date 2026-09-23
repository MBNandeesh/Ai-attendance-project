
from fastapi.testclient import TestClient

from tests.conftest import create_teacher


def _create_student(client: TestClient, name: str = "Test Student") -> dict:
    """Create a student row directly via dev registration helper.

    Uses the SQLAlchemy session through the app's test DB.
    """
    from app.db.models import Student
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        student = Student(name=name)
        db.add(student)
        db.commit()
        db.refresh(student)
        return {"student_id": student.student_id, "name": student.name}
    finally:
        db.close()


def _student_headers(client: TestClient, student_id: int) -> dict:
    resp = client.post("/api/v1/auth/student/dev-login", json={"student_id": student_id})
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_teacher_enrolls_student_in_subject(client, teacher):
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": "CS201", "name": "Data Structures"},
    ).json()

    student = _create_student(client, "Alice")
    resp = client.post(
        f"/api/v1/subjects/{subject['subject_id']}/enroll",
        headers=teacher["headers"],
        json={"student_id": student["student_id"]},
    )
    assert resp.status_code == 201


def test_double_enroll_rejected(client, teacher):
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": "CS202", "name": "Algorithms"},
    ).json()

    student = _create_student(client, "Bob")
    client.post(
        f"/api/v1/subjects/{subject['subject_id']}/enroll",
        headers=teacher["headers"],
        json={"student_id": student["student_id"]},
    )
    resp = client.post(
        f"/api/v1/subjects/{subject['subject_id']}/enroll",
        headers=teacher["headers"],
        json={"student_id": student["student_id"]},
    )
    assert resp.status_code == 409


def test_enrolled_students_listed(client, teacher):
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": "CS203", "name": "Databases"},
    ).json()

    student = _create_student(client, "Carol")
    client.post(
        f"/api/v1/subjects/{subject['subject_id']}/enroll",
        headers=teacher["headers"],
        json={"student_id": student["student_id"]},
    )

    resp = client.get(
        f"/api/v1/subjects/{subject['subject_id']}/students",
        headers=teacher["headers"],
    )
    assert resp.status_code == 200
    names = [s["name"] for s in resp.json()]
    assert "Carol" in names


def test_unenroll_works(client, teacher):
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": "CS204", "name": "Networks"},
    ).json()

    student = _create_student(client, "Dave")
    client.post(
        f"/api/v1/subjects/{subject['subject_id']}/enroll",
        headers=teacher["headers"],
        json={"student_id": student["student_id"]},
    )
    resp = client.delete(
        f"/api/v1/subjects/{subject['subject_id']}/enroll/{student['student_id']}",
        headers=teacher["headers"],
    )
    assert resp.status_code == 200

    # Re-unenroll should 404
    resp = client.delete(
        f"/api/v1/subjects/{subject['subject_id']}/enroll/{student['student_id']}",
        headers=teacher["headers"],
    )
    assert resp.status_code == 404


def test_cannot_enroll_into_other_teachers_subject(client, teacher):
    other = create_teacher(client)
    subject = client.post(
        "/api/v1/subjects",
        headers=other["headers"],
        json={"subject_code": "SEC1", "name": "Secret Subject"},
    ).json()

    student = _create_student(client, "Eve")
    resp = client.post(
        f"/api/v1/subjects/{subject['subject_id']}/enroll",
        headers=teacher["headers"],
        json={"student_id": student["student_id"]},
    )
    assert resp.status_code == 404


def test_student_joins_by_code(client, teacher):
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": "CS301", "name": "Operating Systems"},
    ).json()

    student = _create_student(client, "Frank")
    headers = _student_headers(client, student["student_id"])

    resp = client.post(f"/api/v1/join/{subject['join_code']}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["subject_id"] == subject["subject_id"]

    # Student sees the subject in their list
    mine = client.get("/api/v1/auth/student/me/subjects", headers=headers)
    codes = [s["subject_code"] for s in mine.json()]
    assert "CS301" in codes


def test_join_invalid_code_404(client):
    student = _create_student(client, "Grace")
    headers = _student_headers(client, student["student_id"])
    resp = client.post("/api/v1/join/NOPE1234", headers=headers)
    assert resp.status_code == 404


def test_join_twice_conflict(client, teacher):
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": "CS302", "name": "Machine Learning"},
    ).json()

    student = _create_student(client, "Heidi")
    headers = _student_headers(client, student["student_id"])

    assert client.post(f"/api/v1/join/{subject['join_code']}", headers=headers).status_code == 200
    resp = client.post(f"/api/v1/join/{subject['join_code']}", headers=headers)
    assert resp.status_code == 409


def test_join_is_case_insensitive(client, teacher):
    subject = client.post(
        "/api/v1/subjects",
        headers=teacher["headers"],
        json={"subject_code": "CS303", "name": "Compilers"},
    ).json()

    student = _create_student(client, "Ivan")
    headers = _student_headers(client, student["student_id"])
    resp = client.post(f"/api/v1/join/{subject['join_code'].lower()}", headers=headers)
    assert resp.status_code == 200
