import base64
import binascii
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.db.models import Student
from app.db.session import get_db
from app.ml.voice import embed_audio_bytes, normalize_voice_embeddings
from app.schemas.voice import VoiceEnrollRequest, VoiceEnrollResponse

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/enroll", response_model=VoiceEnrollResponse)
def enroll_voice(
    body: VoiceEnrollRequest,
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    try:
        audio = base64.b64decode(body.audio_base64, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid base64 audio") from exc

    embedding = embed_audio_bytes(audio)
    if embedding is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Could not process audio — record in a quiet place and speak clearly",
        )

    existing = normalize_voice_embeddings(student.voice_embedding)
    combined = existing.tolist() + [embedding.tolist()]

    student.voice_embedding = json.dumps(combined)
    db.commit()

    return VoiceEnrollResponse(
        student_id=student.student_id,
        samples=len(combined),
        message="Voice profile saved",
    )


@router.get("/status", response_model=VoiceEnrollResponse)
def voice_status(
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    existing = normalize_voice_embeddings(student.voice_embedding)
    return VoiceEnrollResponse(
        student_id=student.student_id,
        samples=existing.shape[0],
        message="Voice enrolled" if existing.shape[0] else "No voice profile yet",
    )
