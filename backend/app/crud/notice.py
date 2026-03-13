from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.db.models.notice import Notice
from app.db.models.user import User
from app.schemas.notice import NoticeCreate, NoticeUpdate


def get_notice(db: Session, notice_id: int) -> Notice | None:
    return db.query(Notice).filter(Notice.id == notice_id).first()


def get_notices(db: Session, skip: int = 0, limit: int = 100) -> List[Notice]:
    return db.query(Notice).order_by(Notice.created_at.desc()).offset(skip).limit(limit).all()


def get_notices_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Notice]:
    # Get notices for the user's role and department
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    query = db.query(Notice)
    
    # Filter by target audience
    if user.role.name == "student":
        query = query.filter(
            (Notice.target_audience.in_(["all", "students"]))
        )
        # If student has department, also include department-specific notices
        if hasattr(user, 'student_profile') and user.student_profile and user.student_profile.department_id:
            query = query.filter(
                (Notice.department_id.is_(None)) |
                (Notice.department_id == user.student_profile.department_id)
            )
    elif user.role.name == "faculty":
        query = query.filter(
            (Notice.target_audience.in_(["all", "faculty"]))
        )
        # If faculty has department, also include department-specific notices
        if hasattr(user, 'faculty_profile') and user.faculty_profile and user.faculty_profile.department_id:
            query = query.filter(
                (Notice.department_id.is_(None)) |
                (Notice.department_id == user.faculty_profile.department_id)
            )
    # else: admin sees all notices
    
    return query.order_by(Notice.created_at.desc()).offset(skip).limit(limit).all()


def get_recent_notices(db: Session, limit: int = 5) -> List[Notice]:
    return db.query(Notice).order_by(Notice.created_at.desc()).limit(limit).all()


def create_notice(db: Session, notice: NoticeCreate) -> Notice:
    db_notice = Notice(**notice.model_dump())
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return db_notice


def update_notice(db: Session, notice_id: int, notice_update: NoticeUpdate) -> Notice | None:
    db_notice = get_notice(db, notice_id)
    if not db_notice:
        return None
    update_data = notice_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_notice, field, value)
    db_notice.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_notice)
    return db_notice


def delete_notice(db: Session, notice_id: int) -> bool:
    db_notice = get_notice(db, notice_id)
    if not db_notice:
        return False
    db.delete(db_notice)
    db.commit()
    return True