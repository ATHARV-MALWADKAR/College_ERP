from datetime import datetime

from pydantic import BaseModel

from app.db.models.assignment import AssignmentStatus


class AssignmentBase(BaseModel):
    title: str
    description: str | None = None
    due_at: datetime
    status: AssignmentStatus | None = None


class AssignmentCreate(AssignmentBase):
    created_by_id: int


class AssignmentRead(AssignmentBase):
    id: int
    created_by_id: int

    class Config:
        from_attributes = True

