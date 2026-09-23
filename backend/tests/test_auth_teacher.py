import uuid


def _unique_username() -> str:
    return f"teacher_{uuid.uuid4().hex[:8]}"


def _register(client, username: str, password: str = "supersecret123"):
    return client.post(
        "/api/v1/auth/teacher/register",
        json={"username": username, "name": "Test User", "password": password},
    )


def _login(client, username: str, password: str = "supersecret123"):
    return client.post(
        "/api/v1/auth/teacher/login",
        json={"username": username, "password": password},
    )


def test_register_teacher_success(client):
    resp = client.post(
        "/api/v1/auth/teacher/register",
        json={"username": _unique_username(), "name": "Alice", "password": "supersecret123"},
    )
    assert resp.status_code == 201
    assert "created" in resp.json()["message"].lower()


def test_register_duplicate_username_fails(client):
    username = _unique_username()
    body = {"username": username, "name": "Alice", "password": "supersecret123"}
    client.post("/api/v1/auth/teacher/register", json=body)
    resp = client.post("/api/v1/auth/teacher/register", json=body)
    assert resp.status_code == 409


def test_register_short_password_rejected(client):
    resp = client.post(
        "/api/v1/auth/teacher/register",
        json={"username": _unique_username(), "name": "Bob", "password": "short"},
    )
    assert resp.status_code == 422


def test_login_success(client):
    username = _unique_username()
    client.post(
        "/api/v1/auth/teacher/register",
        json={"username": username, "name": "Carol", "password": "supersecret123"},
    )
    resp = client.post(
        "/api/v1/auth/teacher/login",
        json={"username": username, "password": "supersecret123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "teacher"
    assert data["access_token"]
    assert data["refresh_token"]


def test_login_wrong_password(client):
    username = _unique_username()
    client.post(
        "/api/v1/auth/teacher/register",
        json={"username": username, "name": "Dave", "password": "supersecret123"},
    )
    resp = client.post(
        "/api/v1/auth/teacher/login",
        json={"username": username, "password": "wrongpassword"},
    )
    assert resp.status_code == 401


def test_me_requires_auth(client):
    resp = client.get("/api/v1/auth/teacher/me")
    assert resp.status_code == 401


def test_me_with_token(client, teacher):
    resp = client.get("/api/v1/auth/teacher/me", headers=teacher["headers"])
    assert resp.status_code == 200
    assert resp.json()["role"] == "teacher"


def test_refresh_returns_new_pair(client):
    username = _unique_username()
    _register(client, username)
    login_resp = _login(client, username)
    refresh_token = login_resp.json()["refresh_token"]

    resp = client.post("/api/v1/auth/teacher/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert resp.json()["access_token"]
    assert resp.json()["refresh_token"]


def test_refresh_rejects_access_token(client, teacher):
    access_token = teacher["headers"]["Authorization"].split(" ")[1]
    resp = client.post("/api/v1/auth/teacher/refresh", json={"refresh_token": access_token})
    assert resp.status_code == 401


def test_refresh_token_cannot_authenticate_routes(client, teacher):
    """SECURITY: a refresh token must never act as an access token."""
    username = _unique_username()
    _register(client, username)
    refresh_token = _login(client, username).json()["refresh_token"]

    headers = {"Authorization": f"Bearer {refresh_token}"}
    resp = client.get("/api/v1/auth/teacher/me", headers=headers)
    assert resp.status_code == 401


def test_access_token_accepted_on_routes(client, teacher):
    resp = client.get("/api/v1/auth/teacher/me", headers=teacher["headers"])
    assert resp.status_code == 200
