from pydantic import BaseModel


class ResultBase(BaseModel):
    student_id: int
    course_code: str
    marks_obtained: float
    max_marks: float
    grade: str | None = None


class ResultCreate(ResultBase):
    pass


class ResultRead(ResultBase):
    id: int

    class Config:
        from_attributes = True

