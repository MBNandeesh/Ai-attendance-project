from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.db.models import Student, Subject, SubjectStudent
from app.db.session import get_db
from app.schemas.subjects import SubjectOut

router = APIRouter(prefix="/join", tags=["join"])


def _subject_out(db: Session, subject: Subject) -> SubjectOut:
    total = db.scalar(
        select(func.count(SubjectStudent.student_id)).where(
            SubjectStudent.subject_id == subject.subject_id
        )
    )
    return SubjectOut(
        subject_id=subject.subject_id,
        subject_code=subject.subject_code,
        name=subject.name,
        section=subject.section,
        join_code=subject.join_code,
        total_students=total or 0,
    )


@router.post("/{join_code}", response_model=SubjectOut)
def join_subject_by_code(
    join_code: str,
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    subject = db.scalar(select(Subject).where(Subject.join_code == join_code.upper()))
    if subject is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid join code")

    exists = db.scalar(
        select(SubjectStudent).where(
            SubjectStudent.student_id == student.student_id,
            SubjectStudent.subject_id == subject.subject_id,
        )
    )
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Already enrolled in this subject")

    db.add(SubjectStudent(student_id=student.student_id, subject_id=subject.subject_id))
    db.commit()

    return _subject_out(db, subject)
