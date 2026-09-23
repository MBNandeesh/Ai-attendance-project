from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_student
from app.db.models import Student
from app.ml.liveness import analyze_liveness
from app.schemas.liveness import (
    LivenessChallengeOut,
    LivenessVerifyRequest,
    LivenessVerifyResponse,
)
from app.services.challenge_store import issue_challenge, pop_challenge
from app.services.images import ImageDecodeError, decode_base64_image

router = APIRouter(prefix="/liveness", tags=["liveness"])


@router.get("/challenge", response_model=LivenessChallengeOut)
def get_challenge(student: Student = Depends(get_current_student)):
    token, challenge, instruction = issue_challenge()
    return LivenessChallengeOut(session_token=token, challenge=challenge, instruction=instruction)


@router.post("/verify", response_model=LivenessVerifyResponse)
def verify_liveness(
    body: LivenessVerifyRequest,
    student: Student = Depends(get_current_student),
):
    challenge = pop_challenge(body.session_token)
    if challenge is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Invalid or expired challenge — restart the liveness check",
        )

    frames = []
    try:
        for f in body.frames:
            frames.append(decode_base64_image(f))
    except ImageDecodeError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    result = analyze_liveness(frames, challenge)

    score = (
        1.0
        if result["passed"]
        else 0.5 if (result["blink_detected"] or result["pose_verified"])
        else 0.0
    )

    return LivenessVerifyResponse(
        passed=result["passed"],
        score=score,
        reason=result["reason"],
        blink_detected=result["blink_detected"],
        pose_verified=result["pose_verified"],
    )
