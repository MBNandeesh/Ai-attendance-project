from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str, role: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "role": role, "type": "access", "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str, role: str) -> str:
    expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
    payload = {"sub": subject, "role": role, "type": "refresh", "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict | None:
    """Return the token payload, or None if invalid/expired."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None
    return payload if payload.get("type") in ("access", "refresh") else None
