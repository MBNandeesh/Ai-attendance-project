from pydantic import BaseModel, Field


class SubjectCreate(BaseModel):
    subject_code: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=128)
    section: str = Field(default="-", max_length=32)


class SubjectOut(BaseModel):
    subject_id: int
    subject_code: str
    name: str
    section: str
    join_code: str
    total_students: int

    model_config = {"from_attributes": True}


class EnrollRequest(BaseModel):
    student_id: int


class EnrolledStudentOut(BaseModel):
    student_id: int
    name: str

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    message: str
