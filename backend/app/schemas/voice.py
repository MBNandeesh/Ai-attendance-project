from pydantic import BaseModel, Field


class VoiceEnrollRequest(BaseModel):
    audio_base64: str = Field(description="Base64-encoded recording of the student speaking")


class VoiceEnrollResponse(BaseModel):
    student_id: int
    samples: int
    message: str


class BulkAudioRequest(BaseModel):
    audio_base64: str = Field(description="Base64-encoded classroom audio")
