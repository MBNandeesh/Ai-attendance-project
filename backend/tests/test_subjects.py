from tests.conftest import create_teacher


def _create_subject(client, headers, code="CS101", name="Intro to CS"):
    return client.post(
        "/api/v1/subjects",
        headers=headers,
        json={"subject_code": code, "name": name, "section": "A"},
    )


def test_create_subject_returns_unique_join_code(client, teacher):
    resp = _create_subject(client, teacher["headers"])
    assert resp.status_code == 201
    data = resp.json()
    assert data["subject_code"] == "CS101"
    assert len(data["join_code"]) == 8
    assert data["total_students"] == 0


def test_create_subject_requires_auth(client):
    resp = client.post(
        "/api/v1/subjects",
        json={"subject_code": "CS101", "name": "Intro"},
    )
    assert resp.status_code == 401


def test_duplicate_subject_code_rejected_for_same_teacher(client, teacher):
    _create_subject(client, teacher["headers"], code="CS101")
    resp = _create_subject(client, teacher["headers"], code="CS101", name="Another")
    assert resp.status_code == 409


def test_same_code_allowed_across_teachers(client, teacher):
    _create_subject(client, teacher["headers"], code="CS101")
    other = create_teacher(client)
    resp = _create_subject(client, other["headers"], code="CS101", name="Other section")
    assert resp.status_code == 201


def test_list_subjects_returns_only_own(client, teacher):
    other_teacher = create_teacher(client)
    _create_subject(client, teacher["headers"], code="MINE1")
    _create_subject(client, other_teacher["headers"], code="OTHER1")

    resp = client.get("/api/v1/subjects", headers=teacher["headers"])
    assert resp.status_code == 200
    codes = [s["subject_code"] for s in resp.json()]
    assert "MINE1" in codes
    assert "OTHER1" not in codes


def test_join_codes_are_unique_across_subjects(client, teacher):
    s1 = _create_subject(client, teacher["headers"], code="A1").json()
    s2 = _create_subject(client, teacher["headers"], code="A2").json()
    assert s1["join_code"] != s2["join_code"]
