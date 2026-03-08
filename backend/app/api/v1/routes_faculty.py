from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import RequireFaculty
from app.db.session import get_db


router = APIRouter()


@router.get("/faculty/dashboard")
def get_faculty_dashboard(
    current_user: RequireFaculty,
    db: Session = Depends(get_db),
) -> dict:
    return {
        "summary": {
            "today_classes": 0,
            "pending_evaluations": 0,
        }
    }

