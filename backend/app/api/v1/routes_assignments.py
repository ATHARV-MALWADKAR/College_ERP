from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db


router = APIRouter()


@router.get("/assignments")
def list_assignments(
    db: Session = Depends(get_db),
) -> dict:
    return {"items": []}

