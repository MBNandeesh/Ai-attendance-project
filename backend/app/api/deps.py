from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.models import Student, Teacher
from app.db.session import get_db

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_teacher(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Teacher:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")

    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("role") != "teacher":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")

    teacher = db.get(Teacher, int(payload["sub"]))
    if teacher is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Teacher not found")
    return teacher


def get_current_student(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Student:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")

    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("role") != "student":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")

    student = db.get(Student, int(payload["sub"]))
    if student is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Student not found")
    return student
