from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import RequireFaculty
from app.db.session import get_db
from app.services.dashboard import get_faculty_dashboard_data


router = APIRouter()


@router.get("/faculty/dashboard")
def get_faculty_dashboard(
    current_user: RequireFaculty,
    db: Session = Depends(get_db),
) -> dict:
    return get_faculty_dashboard_data(db, current_user.id)

