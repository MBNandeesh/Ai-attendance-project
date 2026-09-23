"""Unique join-code generation for subjects."""

import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Subject

# Unambiguous alphabet: no 0/O, 1/I/L to avoid misreading codes.
_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
CODE_LENGTH = 8


def _new_code() -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(CODE_LENGTH))


def generate_unique_join_code(db: Session) -> str:
    """Generate a join code guaranteed not to exist in the subjects table."""
    while True:
        code = _new_code()
        exists = db.scalar(select(Subject).where(Subject.join_code == code))
        if exists is None:
            return code
