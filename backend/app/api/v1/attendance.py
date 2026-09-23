import csv
import io

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_student, get_current_teacher
from app.db.models import (
    AttendanceLog,
    AttendanceSession,
    Student,
    Subject,
    SubjectStudent,
    Teacher,
)
from app.db.session import get_db
from app.ml import face as face_pipeline
from app.ml import voice as voice_pipeline
from app.ml.store import load_known_faces
from app.schemas.attendance import (
    AttendanceMarkResponse,
    AttendanceRecordOut,
    FaceAttendanceRequest,
    SessionCreate,
    SessionOut,
    VoiceAttendanceRequest,
)
from app.services.images import ImageDecodeError, decode_base64_image

router = APIRouter(prefix="/attendance", tags=["attendance"])


def _own_subject(db: Session, subject_id: int, teacher: Teacher) -> Subject:
    subject = db.get(Subject, subject_id)
    if subject is None or subject.teacher_id != teacher.teacher_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    return subject


def _own_session(db: Session, session_id: int, teacher: Teacher) -> AttendanceSession:
    session = db.get(AttendanceSession, session_id)
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    _own_subject(db, session.subject_id, teacher)
    return session


def _enrolled_students(db: Session, subject_id: int) -> list[Student]:
    return db.execute(
        select(Student)
        .join(SubjectStudent, SubjectStudent.student_id == Student.student_id)
        .where(SubjectStudent.subject_id == subject_id)
        .order_by(Student.name)
    ).scalars().all()


def _mark_attendance(
    db: Session,
    session: AttendanceSession,
    present_ids: set[int],
    method: str,
    liveness_score: float | None = None,
) -> AttendanceMarkResponse:
    students = _enrolled_students(db, session.subject_id)
    if not students:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No students enrolled in this subject")

    # One log row per student per session (unique constraint protects duplicates).
    existing = {
        log.student_id
        for log in db.execute(
            select(AttendanceLog).where(AttendanceLog.session_id == session.session_id)
        ).scalars()
    }

    entries = []
    for student in students:
        is_present = student.student_id in present_ids
        if student.student_id not in existing:
            db.add(
                AttendanceLog(
                    student_id=student.student_id,
                    session_id=session.session_id,
                    is_present=is_present,
                    method=method,
                    liveness_score=liveness_score if is_present else None,
                )
            )
        entries.append(
            {
                "student_id": student.student_id,
                "name": student.name,
                "is_present": is_present,
                "method": method if is_present else None,
            }
        )

    db.commit()

    return AttendanceMarkResponse(
        session_id=session.session_id,
        total_students=len(students),
        present_count=sum(1 for e in entries if e["is_present"]),
        entries=entries,
    )


@router.post("/sessions", response_model=SessionOut, status_code=201)
def create_session(
    body: SessionCreate,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    subject = _own_subject(db, body.subject_id, teacher)
    session = AttendanceSession(subject_id=subject.subject_id, method=body.method)
    db.add(session)
    db.commit()
    db.refresh(session)

    return SessionOut(
        session_id=session.session_id,
        subject_id=session.subject_id,
        method=session.method,
        started_at=session.started_at.isoformat(),
    )


@router.post("/face", response_model=AttendanceMarkResponse)
def face_attendance(
    body: FaceAttendanceRequest,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    session = _own_session(db, body.session_id, teacher)

    known = load_known_faces(db, force_refresh=True)
    if not known:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No students have face profiles yet")

    present_ids: set[int] = set()
    for image_b64 in body.images:
        try:
            image = decode_base64_image(image_b64)
        except ImageDecodeError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

        for match in face_pipeline.identify_faces(image, known):
            present_ids.add(match["student_id"])

    return _mark_attendance(
        db, session, present_ids, method="face", liveness_score=body.liveness_score
    )


@router.post("/voice", response_model=AttendanceMarkResponse)
def voice_attendance(
    body: VoiceAttendanceRequest,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    import base64
    import binascii

    session = _own_session(db, body.session_id, teacher)

    try:
        audio = base64.b64decode(body.audio_base64, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid base64 audio") from exc

    students = _enrolled_students(db, session.subject_id)
    known: dict[int, any] = {}
    for student in students:
        matrix = voice_pipeline.normalize_voice_embeddings(student.voice_embedding)
        if matrix.shape[0]:
            known[student.student_id] = matrix

    if not known:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No enrolled students have voice profiles")

    detected = voice_pipeline.process_bulk_audio(audio, known)
    return _mark_attendance(db, session, set(detected.keys()), method="voice")


@router.get("/sessions/{session_id}", response_model=AttendanceMarkResponse)
def get_session_results(
    session_id: int,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    session = _own_session(db, session_id, teacher)
    students = _enrolled_students(db, session.subject_id)

    logs = {
        log.student_id: log
        for log in db.execute(
            select(AttendanceLog).where(AttendanceLog.session_id == session.session_id)
        ).scalars()
    }

    entries = [
        {
            "student_id": s.student_id,
            "name": s.name,
            "is_present": logs[s.student_id].is_present if s.student_id in logs else False,
            "method": logs[s.student_id].method if s.student_id in logs else None,
        }
        for s in students
    ]

    return AttendanceMarkResponse(
        session_id=session.session_id,
        total_students=len(students),
        present_count=sum(1 for e in entries if e["is_present"]),
        entries=entries,
    )


def _teacher_records(db: Session, teacher: Teacher) -> list[AttendanceRecordOut]:
    sessions = db.execute(
        select(AttendanceSession)
        .join(Subject, Subject.subject_id == AttendanceSession.subject_id)
        .where(Subject.teacher_id == teacher.teacher_id)
        .order_by(AttendanceSession.started_at.desc())
    ).scalars().all()

    return _build_records(db, sessions)


def _build_records(db: Session, sessions) -> list[AttendanceRecordOut]:
    records = []
    for session in sessions:
        subject = db.get(Subject, session.subject_id)
        logs = db.execute(
            select(AttendanceLog).where(AttendanceLog.session_id == session.session_id)
        ).scalars().all()

        for log in logs:
            student = db.get(Student, log.student_id)
            records.append(
                AttendanceRecordOut(
                    attendance_id=log.attendance_id,
                    session_id=session.session_id,
                    subject_id=subject.subject_id,
                    subject_name=subject.name,
                    subject_code=subject.subject_code,
                    student_id=student.student_id,
                    student_name=student.name,
                    is_present=log.is_present,
                    method=log.method,
                    started_at=session.started_at.isoformat(),
                )
            )
    return records


@router.get("/records", response_model=list[AttendanceRecordOut])
def teacher_records(
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return _teacher_records(db, teacher)


@router.get("/records/export", response_class=StreamingResponse)
def export_records_csv(
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    records = _teacher_records(db, teacher)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "session_id",
            "date",
            "subject_code",
            "subject",
            "student_id",
            "student",
            "status",
            "method",
        ]
    )
    for r in records:
        writer.writerow(
            [
                r.session_id,
                r.started_at[:19].replace("T", " "),
                r.subject_code,
                r.subject_name,
                r.student_id,
                r.student_name,
                "Present" if r.is_present else "Absent",
                r.method,
            ]
        )

    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance_records.csv"},
    )


@router.get("/me", response_model=list[AttendanceRecordOut])
def student_records(
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    logs = db.execute(
        select(AttendanceLog).where(AttendanceLog.student_id == student.student_id)
    ).scalars().all()

    records = []
    for log in logs:
        session = db.get(AttendanceSession, log.session_id)
        subject = db.get(Subject, session.subject_id)
        records.append(
            AttendanceRecordOut(
                attendance_id=log.attendance_id,
                session_id=session.session_id,
                subject_id=subject.subject_id,
                subject_name=subject.name,
                subject_code=subject.subject_code,
                student_id=student.student_id,
                student_name=student.name,
                is_present=log.is_present,
                method=log.method,
                started_at=session.started_at.isoformat(),
            )
        )
    return records
