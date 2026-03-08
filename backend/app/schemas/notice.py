from datetime import datetime

from pydantic import BaseModel


class NoticeBase(BaseModel):
    title: str
    content: str


class NoticeCreate(NoticeBase):
    created_by_id: int


class NoticeRead(NoticeBase):
    id: int
    created_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True

