from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TargetAudience(str, Enum):
    ALL = "all"
    STUDENTS = "students"
    FACULTY = "faculty"


class NoticeBase(BaseModel):
    title: str
    content: str
    target_audience: TargetAudience = TargetAudience.ALL
    department_id: int | None = None


class NoticeCreate(NoticeBase):
    created_by_id: int


class NoticeRead(NoticeBase):
    id: int
    created_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True


class NoticeUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    target_audience: TargetAudience | None = None
    department_id: int | None = None

