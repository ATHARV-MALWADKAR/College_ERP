from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import RequireStudent
from app.db.session import get_db
from app.services.dashboard import get_student_dashboard_data


router = APIRouter()


@router.get("/students/dashboard")
def get_student_dashboard(
    current_user: RequireStudent,
    db: Session = Depends(get_db),
) -> dict:
    return get_student_dashboard_data(db, current_user.id)

