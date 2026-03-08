from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db


router = APIRouter()


@router.get("/notices")
def list_notices(
    db: Session = Depends(get_db),
) -> dict:
    return {"items": []}

