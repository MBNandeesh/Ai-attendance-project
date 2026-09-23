from pydantic import BaseModel, Field


class LivenessChallengeOut(BaseModel):
    session_token: str
    challenge: str
    instruction: str


class LivenessVerifyRequest(BaseModel):
    session_token: str
    frames: list[str] = Field(
        min_length=5,
        max_length=60,
        description="Base64 JPEG frames sampled across the challenge (~1-3s)",
    )


class LivenessVerifyResponse(BaseModel):
    passed: bool
    score: float
    reason: str
    blink_detected: bool
    pose_verified: bool
