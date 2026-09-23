"""Bridge between DB-stored JSON embeddings and numpy matrices, with a TTL cache."""

import json
import time

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Student
from app.ml.face import normalize_embeddings

_CACHE: dict[int, np.ndarray] = {}
_CACHE_TIME = 0.0
_CACHE_DB_ID = id(None)  # identity of the last DB session seen
CACHE_TTL_SECONDS = 30.0  # new enrollments appear within 30s without cache-bust complexity


def load_known_faces(db: Session, force_refresh: bool = False) -> dict[int, np.ndarray]:
    """Return {student_id: (N,128) matrix} of all enrolled face embeddings."""
    global _CACHE, _CACHE_TIME, _CACHE_DB_ID

    now = time.monotonic()
    db_is_same = _CACHE_DB_ID == id(db)
    if (
        not force_refresh
        and _CACHE
        and db_is_same
        and (now - _CACHE_TIME) < CACHE_TTL_SECONDS
    ):
        return _CACHE

    students = db.execute(
        select(Student).where(Student.face_embedding.is_not(None))
    ).scalars().all()

    known: dict[int, np.ndarray] = {}
    for student in students:
        try:
            matrix = normalize_embeddings(json.loads(student.face_embedding))
        except (ValueError, TypeError):
            continue
        if matrix.shape[0]:
            known[student.student_id] = matrix

    _CACHE = known
    _CACHE_TIME = now
    _CACHE_DB_ID = id(db)
    return known


def invalidate_cache() -> None:
    """Force the next load to hit the DB (called after enrollment changes)."""
    global _CACHE, _CACHE_TIME
    _CACHE = {}
    _CACHE_TIME = 0.0
