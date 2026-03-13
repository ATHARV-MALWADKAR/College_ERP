from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.db.models.timetable import TimetableEntry
from app.schemas.timetable import TimetableEntryCreate, TimetableEntryBase


def get_timetable_entry(db: Session, entry_id: int) -> TimetableEntry | None:
    return db.query(TimetableEntry).filter(TimetableEntry.id == entry_id).first()


def get_timetable_for_course(db: Session, course_id: int) -> List[TimetableEntry]:
    return (
        db.query(TimetableEntry)
        .filter(TimetableEntry.course_id == course_id)
        .order_by(TimetableEntry.day_of_week, TimetableEntry.start_time)
        .all()
    )


def get_timetable_for_faculty(db: Session, faculty_id: int) -> List[TimetableEntry]:
    return (
        db.query(TimetableEntry)
        .filter(TimetableEntry.faculty_id == faculty_id)
        .order_by(TimetableEntry.day_of_week, TimetableEntry.start_time)
        .all()
    )


def create_timetable_entry(db: Session, entry: TimetableEntryCreate) -> TimetableEntry:
    db_entry = TimetableEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_timetable_entry(db: Session, entry_id: int, entry_update: TimetableEntryBase) -> TimetableEntry | None:
    db_entry = get_timetable_entry(db, entry_id)
    if not db_entry:
        return None
    update_data = entry_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entry, field, value)
    db_entry.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_entry)
    return db_entry


def delete_timetable_entry(db: Session, entry_id: int) -> bool:
    db_entry = get_timetable_entry(db, entry_id)
    if not db_entry:
        return False
    db.delete(db_entry)
    db.commit()
    return True
