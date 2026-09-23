import json

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.core.security import create_access_token, create_refresh_token
from app.db.models import Student
from app.db.session import get_db
from app.ml import face as face_pipeline
from app.ml.store import invalidate_cache, load_known_faces
from app.schemas.students import (
    FaceLoginRequest,
    FaceLoginResponse,
    FaceSamplesUpdateRequest,
    StudentOut,
    StudentRegisterRequest,
)
from app.services.images import ImageDecodeError, decode_base64_image

router = APIRouter(prefix="/students", tags=["students"])


def _tokens(student: Student) -> FaceLoginResponse:
    return FaceLoginResponse(
        access_token=create_access_token(str(student.student_id), "student"),
        refresh_token=create_refresh_token(str(student.student_id), "student"),
        role="student",
        user_id=student.student_id,
        name=student.name,
    )


def _single_face_embedding(image_b64: str) -> list[float]:
    """Decode an image, require exactly one face, return its embedding."""
    try:
        image = decode_base64_image(image_b64)
    except ImageDecodeError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    encodings = face_pipeline.get_face_embeddings(image)
    if not encodings:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "No face detected in the image"
        )
    if len(encodings) > 1:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Multiple faces detected — capture only your face",
        )
    return encodings[0].tolist()


@router.post("/register", response_model=FaceLoginResponse, status_code=201)
def register_student(body: StudentRegisterRequest, db: Session = Depends(get_db)):
    embedding = _single_face_embedding(body.face_image)

    known = load_known_faces(db, force_refresh=True)
    duplicate_id, _distance = face_pipeline.find_duplicate_face(np.array(embedding), known)
    if duplicate_id is not None:
        existing = db.get(Student, duplicate_id)
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"This face is already registered as {existing.name if existing else 'a student'}",
            )

    student = Student(
        name=body.name,
        face_embedding=json.dumps([embedding]),
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    invalidate_cache()
    return _tokens(student)


@router.post("/face-login", response_model=FaceLoginResponse)
def face_login(body: FaceLoginRequest, db: Session = Depends(get_db)):
    try:
        image = decode_base64_image(body.face_image)
    except ImageDecodeError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    encodings = face_pipeline.get_face_embeddings(image)
    if not encodings:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "No face detected — position your face clearly",
        )
    if len(encodings) > 1:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Multiple faces detected — capture only your face",
        )

    known = load_known_faces(db, force_refresh=True)
    student_id = face_pipeline.identify_faces_single(encodings[0], known)
    if student_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Face not recognized")

    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Face not recognized")

    return _tokens(student)


@router.post("/me/face-samples", response_model=StudentOut)
def add_face_samples(
    body: FaceSamplesUpdateRequest,
    student: Student = Depends(get_current_student),  # noqa: B008
    db: Session = Depends(get_db),
):
    new_embeddings = [_single_face_embedding(img) for img in body.face_images]

    existing = face_pipeline.normalize_embeddings(json.loads(student.face_embedding or "null"))
    combined = existing.tolist() + new_embeddings

    student.face_embedding = json.dumps(combined)
    db.commit()
    invalidate_cache()

    return StudentOut(student_id=student.student_id, name=student.name)
