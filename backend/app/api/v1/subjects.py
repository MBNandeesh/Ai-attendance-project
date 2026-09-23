from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_teacher
from app.db.models import Student, Subject, SubjectStudent, Teacher
from app.db.session import get_db
from app.schemas.subjects import (
    EnrolledStudentOut,
    EnrollRequest,
    MessageResponse,
    SubjectCreate,
    SubjectOut,
)
from app.services.join_code import generate_unique_join_code

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("", response_model=SubjectOut, status_code=201)
def create_subject(
    body: SubjectCreate,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    duplicate = db.scalar(
        select(Subject).where(
            Subject.teacher_id == teacher.teacher_id,
            Subject.subject_code == body.subject_code,
        )
    )
    if duplicate:
        raise HTTPException(status.HTTP_409_CONFLICT, "You already have a subject with this code")

    subject = Subject(
        subject_code=body.subject_code,
        name=body.name,
        section=body.section,
        teacher_id=teacher.teacher_id,
        join_code=generate_unique_join_code(db),
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)

    return SubjectOut(
        subject_id=subject.subject_id,
        subject_code=subject.subject_code,
        name=subject.name,
        section=subject.section,
        join_code=subject.join_code,
        total_students=0,
    )


@router.get("", response_model=list[SubjectOut])
def list_my_subjects(
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    rows = db.execute(
        select(
            Subject,
            func.count(SubjectStudent.student_id).label("total_students"),
        )
        .outerjoin(SubjectStudent, SubjectStudent.subject_id == Subject.subject_id)
        .where(Subject.teacher_id == teacher.teacher_id)
        .group_by(Subject.subject_id)
        .order_by(Subject.created_at.desc())
    ).all()

    return [
        SubjectOut(
            subject_id=subject.subject_id,
            subject_code=subject.subject_code,
            name=subject.name,
            section=subject.section,
            join_code=subject.join_code,
            total_students=count,
        )
        for subject, count in rows
    ]


@router.get("/{subject_id}/students", response_model=list[EnrolledStudentOut])
def list_enrolled_students(
    subject_id: int,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    _require_own_subject(db, subject_id, teacher)

    rows = db.execute(
        select(Student)
        .join(SubjectStudent, SubjectStudent.student_id == Student.student_id)
        .where(SubjectStudent.subject_id == subject_id)
        .order_by(Student.name)
    ).scalars().all()

    return [EnrolledStudentOut(student_id=s.student_id, name=s.name) for s in rows]


@router.post("/{subject_id}/enroll", response_model=MessageResponse, status_code=201)
def enroll_student(
    subject_id: int,
    body: EnrollRequest,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    _require_own_subject(db, subject_id, teacher)

    student = db.get(Student, body.student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")

    exists = db.scalar(
        select(SubjectStudent).where(
            SubjectStudent.student_id == body.student_id,
            SubjectStudent.subject_id == subject_id,
        )
    )
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Student already enrolled")

    db.add(SubjectStudent(student_id=body.student_id, subject_id=subject_id))
    db.commit()
    return MessageResponse(message=f"{student.name} enrolled successfully")


@router.delete("/{subject_id}/enroll/{student_id}", response_model=MessageResponse)
def unenroll_student(
    subject_id: int,
    student_id: int,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    _require_own_subject(db, subject_id, teacher)

    row = db.get(SubjectStudent, (student_id, subject_id))
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Enrollment not found")

    db.delete(row)
    db.commit()
    return MessageResponse(message="Student unenrolled")


def _require_own_subject(db: Session, subject_id: int, teacher: Teacher) -> Subject:
    subject = db.get(Subject, subject_id)
    if subject is None or subject.teacher_id != teacher.teacher_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    return subject
