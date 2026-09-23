from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_teacher
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.models import Teacher
from app.db.session import get_db
from app.schemas.auth import (
    MessageResponse,
    RefreshRequest,
    TeacherLoginRequest,
    TeacherRegisterRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth/teacher", tags=["auth"])


def _token_response(teacher: Teacher) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(str(teacher.teacher_id), "teacher"),
        refresh_token=create_refresh_token(str(teacher.teacher_id), "teacher"),
        role="teacher",
        user_id=teacher.teacher_id,
        name=teacher.name,
    )


@router.post("/register", response_model=MessageResponse, status_code=201)
def register_teacher(body: TeacherRegisterRequest, db: Session = Depends(get_db)):
    exists = db.scalar(select(Teacher).where(Teacher.username == body.username))
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")

    teacher = Teacher(username=body.username, name=body.name, password=hash_password(body.password))
    db.add(teacher)
    db.commit()
    return MessageResponse(message="Account created. You can log in now.")


@router.post("/login", response_model=TokenResponse)
def login_teacher(body: TeacherLoginRequest, db: Session = Depends(get_db)):
    teacher = db.scalar(select(Teacher).where(Teacher.username == body.username))
    if teacher is None or not verify_password(body.password, teacher.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid username or password")

    return _token_response(teacher)


@router.post("/refresh", response_model=TokenResponse)
def refresh_tokens(body: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(body.refresh_token)
    if payload is None or payload.get("role") != "teacher" or payload.get("type") != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")

    teacher = db.get(Teacher, int(payload["sub"]))
    if teacher is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Teacher not found")

    return _token_response(teacher)


@router.get("/me", response_model=TokenResponse)
def read_teacher(teacher: Teacher = Depends(get_current_teacher)):
    return TokenResponse(
        access_token="",
        refresh_token="",
        role="teacher",
        user_id=teacher.teacher_id,
        name=teacher.name,
    )
