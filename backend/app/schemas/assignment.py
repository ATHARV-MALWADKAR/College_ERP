from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class AssignmentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class AssignmentBase(BaseModel):
    title: str
    description: str | None = None
    due_at: datetime
    status: AssignmentStatus | None = None


class AssignmentCreate(AssignmentBase):
    subject_id: int
    created_by_id: int


class AssignmentRead(AssignmentBase):
    id: int
    subject_id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_at: datetime | None = None
    status: AssignmentStatus | None = None

