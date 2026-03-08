from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    code = Column(String(30), unique=True, nullable=False, index=True)
    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    duration_years = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = relationship("Department", back_populates="courses")
    subjects = relationship("Subject", back_populates="course")
    students = relationship("Student", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    timetable_entries = relationship("TimetableEntry", back_populates="course")
