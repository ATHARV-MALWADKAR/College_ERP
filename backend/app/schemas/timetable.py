from datetime import time

from pydantic import BaseModel


class TimetableEntryBase(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    course_code: str
    room: str | None = None
    faculty_id: int


class TimetableEntryCreate(TimetableEntryBase):
    pass


class TimetableEntryRead(TimetableEntryBase):
    id: int

    class Config:
        from_attributes = True

