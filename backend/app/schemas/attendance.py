from datetime import date

from pydantic import BaseModel

from app.db.models.attendance import AttendanceStatus


class AttendanceBase(BaseModel):
    student_id: int
    date: date
    status: AttendanceStatus


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    id: int

    class Config:
        from_attributes = True

