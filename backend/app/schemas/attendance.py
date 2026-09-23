from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    subject_id: int
    method: str = Field(pattern="^(face|voice|manual)$")


class SessionOut(BaseModel):
    session_id: int
    subject_id: int
    method: str
    started_at: str

    model_config = {"from_attributes": True}


class FaceAttendanceRequest(BaseModel):
    session_id: int
    images: list[str] = Field(min_length=1, description="Base64 classroom photos")
    liveness_score: float | None = Field(default=None, ge=0.0, le=1.0)


class VoiceAttendanceRequest(BaseModel):
    session_id: int
    audio_base64: str


class AttendanceEntryOut(BaseModel):
    student_id: int
    name: str
    is_present: bool
    method: str | None


class AttendanceMarkResponse(BaseModel):
    session_id: int
    total_students: int
    present_count: int
    entries: list[AttendanceEntryOut]


class AttendanceRecordOut(BaseModel):
    attendance_id: int
    session_id: int
    subject_id: int
    subject_name: str
    subject_code: str
    student_id: int
    student_name: str
    is_present: bool
    method: str
    started_at: str
