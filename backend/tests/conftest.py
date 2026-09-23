"""Shared pytest fixtures. Uses an isolated SQLite DB per session."""

import os

# Must be set before app modules import settings.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_attendance.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-pytest-only-32b")

# Start every test session from a clean database.
if os.path.exists("test_attendance.db"):
    os.remove("test_attendance.db")

import pytest
from fastapi.testclient import TestClient

from app.db.session import init_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def _setup_db():
    init_db()
    yield


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


def create_teacher(client: TestClient) -> dict:
    """Register + login a unique teacher; returns auth headers and profile."""
    import uuid

    username = f"teacher_{uuid.uuid4().hex[:8]}"
    client.post(
        "/api/v1/auth/teacher/register",
        json={"username": username, "name": "Test Teacher", "password": "supersecret123"},
    )
    resp = client.post(
        "/api/v1/auth/teacher/login",
        json={"username": username, "password": "supersecret123"},
    )
    data = resp.json()
    return {
        "headers": {"Authorization": f"Bearer {data['access_token']}"},
        "user_id": data["user_id"],
        "username": username,
    }


@pytest.fixture()
def teacher(client):
    return create_teacher(client)
