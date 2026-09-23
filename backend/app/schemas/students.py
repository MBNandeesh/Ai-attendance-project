from pydantic import BaseModel, Field


class StudentRegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    face_image: str = Field(
        description="Base64-encoded JPEG/PNG of the student's face"
    )
    voice_embedding: list[float] | None = Field(
        default=None,
        description="Optional 256-D voice embedding",
    )


class FaceLoginRequest(BaseModel):
    face_image: str = Field(description="Base64-encoded JPEG/PNG of the student's face")


class StudentOut(BaseModel):
    student_id: int
    name: str

    model_config = {"from_attributes": True}


class FaceLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    name: str
    recognized: bool = True


class DuplicateFaceResponse(BaseModel):
    duplicate: bool
    existing_student_id: int | None = None
    existing_name: str | None = None
    distance: float | None = None


class FaceSamplesUpdateRequest(BaseModel):
    face_images: list[str] = Field(min_length=1, description="Base64 images, one face each")
