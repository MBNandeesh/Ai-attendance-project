"""In-memory challenge store for liveness sessions.

A single-worker deployment is assumed (uvicorn default). For multi-worker
production, swap this for Redis — the interface is intentionally tiny.
"""

import secrets
import time

TTL_SECONDS = 120

_challenges: dict[str, tuple[str, float]] = {}  # token -> (challenge, issued_at)

CHALLENGE_INSTRUCTIONS = {
    "turn_left": "Slowly turn your head to your LEFT",
    "turn_right": "Slowly turn your head to your RIGHT",
    "look_up": "Slowly look UP toward the ceiling",
}


def issue_challenge() -> tuple[str, str, str]:
    """Return (session_token, challenge, human instruction)."""
    token = secrets.token_urlsafe(32)
    challenge = secrets.choice(list(CHALLENGE_INSTRUCTIONS.keys()))
    _challenges[token] = (challenge, time.monotonic())
    _gc()
    return token, challenge, CHALLENGE_INSTRUCTIONS[challenge]


def pop_challenge(token: str) -> str | None:
    """Consume a challenge once (single-use). Returns None if unknown/expired."""
    entry = _challenges.pop(token, None)
    if entry is None:
        return None
    challenge, issued_at = entry
    if time.monotonic() - issued_at > TTL_SECONDS:
        return None
    return challenge


def _gc() -> None:
    now = time.monotonic()
    expired = [t for t, (_, issued) in _challenges.items() if now - issued > TTL_SECONDS]
    for t in expired:
        _challenges.pop(t, None)
