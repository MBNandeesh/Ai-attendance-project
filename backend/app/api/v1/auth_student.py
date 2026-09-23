from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.models import Student, Subject, SubjectStudent
from app.db.session import get_db
from app.schemas.auth import RefreshRequest, TokenResponse
from app.schemas.subjects import SubjectOut

router = APIRouter(prefix="/auth/student", tags=["auth"])


def _student_tokens(student: Student) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(str(student.student_id), "student"),
        refresh_token=create_refresh_token(str(student.student_id), "student"),
        role="student",
        user_id=student.student_id,
        name=student.name,
    )


@router.post("/dev-login", response_model=TokenResponse)
def dev_login(body: dict, db: Session = Depends(get_db)):
    """
    TEMPORARY dev-only login: pass {"student_id": 1}.
    Will be replaced by face login in the ML milestone. Disabled in production.
    """
    if settings.environment == "production":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Disabled in production")

    student_id = body.get("student_id")
    student = db.get(Student, int(student_id)) if student_id is not None else None
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")

    return _student_tokens(student)


@router.post("/refresh", response_model=TokenResponse)
def refresh_tokens(body: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(body.refresh_token)
    if payload is None or payload.get("role") != "student" or payload.get("type") != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")

    student = db.get(Student, int(payload["sub"]))
    if student is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Student not found")

    return _student_tokens(student)


@router.get("/me", response_model=TokenResponse)
def read_student(student: Student = Depends(get_current_student)):
    return TokenResponse(
        access_token="",
        refresh_token="",
        role="student",
        user_id=student.student_id,
        name=student.name,
    )


@router.get("/me/subjects", response_model=list[SubjectOut])
def my_subjects(
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    rows = db.execute(
        select(Subject)
        .join(SubjectStudent, SubjectStudent.subject_id == Subject.subject_id)
        .where(SubjectStudent.student_id == student.student_id)
    ).scalars().all()

    return [
        SubjectOut(
            subject_id=s.subject_id,
            subject_code=s.subject_code,
            name=s.name,
            section=s.section,
            join_code=s.join_code,
            total_students=0,
        )
        for s in rows
    ]
