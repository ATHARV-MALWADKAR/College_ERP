from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import RequireAdmin
from app.db.session import get_db


router = APIRouter()


@router.get("/admin/dashboard")
def get_admin_dashboard(
    current_user: RequireAdmin,
    db: Session = Depends(get_db),
) -> dict:
    return {
        "summary": {
            "total_students": 0,
            "total_faculty": 0,
            "active_notices": 0,
        }
    }

