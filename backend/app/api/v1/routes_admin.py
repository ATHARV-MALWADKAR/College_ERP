from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import RequireAdmin
from app.db.session import get_db
from app.services.analytics import get_admin_dashboard_stats

router = APIRouter()


@router.get("/admin/dashboard")
def get_admin_dashboard(
    current_user: RequireAdmin,
    db: Session = Depends(get_db),
) -> dict:
    stats = get_admin_dashboard_stats(db)
    return stats

