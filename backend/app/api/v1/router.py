from fastapi import APIRouter

from app.api.v1 import (
    attendance,
    auth_student,
    auth_teacher,
    join,
    liveness,
    students,
    subjects,
    voice,
)

api_router = APIRouter()
api_router.include_router(auth_teacher.router)
api_router.include_router(auth_student.router)
api_router.include_router(subjects.router)
api_router.include_router(join.router)
api_router.include_router(students.router)
api_router.include_router(voice.router)
api_router.include_router(attendance.router)
api_router.include_router(liveness.router)
