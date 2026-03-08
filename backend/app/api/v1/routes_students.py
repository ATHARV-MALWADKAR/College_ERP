from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import RequireStudent
from app.db.session import get_db


router = APIRouter()


@router.get("/students/dashboard")
def get_student_dashboard(
    current_user: RequireStudent,
    db: Session = Depends(get_db),
) -> dict:
    # Placeholder data to be replaced with real queries.
    return {
        "summary": {
            "attendance_percentage": 0.0,
            "pending_assignments": 0,
            "upcoming_exams": 0,
        }
    }

