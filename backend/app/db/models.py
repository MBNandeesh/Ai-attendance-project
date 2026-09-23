from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    # JSON: list of 128-D face samples
    face_embedding: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON: single embedding list
    voice_embedding: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    enrollments: Mapped[list["SubjectStudent"]] = relationship(back_populates="student")
    logs: Mapped[list["AttendanceLog"]] = relationship(back_populates="student")


class Subject(Base):
    __tablename__ = "subjects"

    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_code: Mapped[str] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(128))
    section: Mapped[str] = mapped_column(String(32), default="-")
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.teacher_id"))
    join_code: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    enrollments: Mapped[list["SubjectStudent"]] = relationship(back_populates="subject")
    sessions: Mapped[list["AttendanceSession"]] = relationship(back_populates="subject")


class SubjectStudent(Base):
    __tablename__ = "subject_students"
    __table_args__ = (UniqueConstraint("student_id", "subject_id", name="uq_student_subject"),)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"), primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"), primary_key=True)

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    subject: Mapped["Subject"] = relationship(back_populates="enrollments")


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.subject_id"))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    method: Mapped[str] = mapped_column(String(16))  # face | voice | manual

    subject: Mapped["Subject"] = relationship(back_populates="sessions")
    logs: Mapped[list["AttendanceLog"]] = relationship(back_populates="session")


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    __table_args__ = (UniqueConstraint("student_id", "session_id", name="uq_student_session"),)

    attendance_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("attendance_sessions.session_id"))
    is_present: Mapped[bool] = mapped_column(Boolean, default=False)
    method: Mapped[str] = mapped_column(String(16), default="face")  # face | voice | manual
    liveness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    student: Mapped["Student"] = relationship(back_populates="logs")
    session: Mapped["AttendanceSession"] = relationship(back_populates="logs")
    corrections: Mapped[list["AttendanceCorrection"]] = relationship(back_populates="log")


class AttendanceCorrection(Base):
    __tablename__ = "attendance_corrections"

    correction_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attendance_id: Mapped[int] = mapped_column(ForeignKey("attendance_logs.attendance_id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.teacher_id"))
    old_value: Mapped[bool]
    new_value: Mapped[bool]
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    log: Mapped["AttendanceLog"] = relationship(back_populates="corrections")
