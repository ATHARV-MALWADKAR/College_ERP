from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    code = Column(String(30), nullable=False)
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    semester = Column(SmallInteger, nullable=False)
    credits = Column(Numeric(4, 2), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("course_id", "code", name="uq_subjects_course_code"),)

    course = relationship("Course", back_populates="subjects")
    attendance_records = relationship("Attendance", back_populates="subject")
    assignments = relationship("Assignment", back_populates="subject")
    results = relationship("Result", back_populates="subject")
    timetable_entries = relationship("TimetableEntry", back_populates="subject")
