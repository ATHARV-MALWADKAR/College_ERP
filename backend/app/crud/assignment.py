from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.db.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate


def get_assignment(db: Session, assignment_id: int) -> Assignment | None:
    return db.query(Assignment).filter(Assignment.id == assignment_id).first()


def get_assignments_by_subject(db: Session, subject_id: int) -> List[Assignment]:
    return db.query(Assignment).filter(Assignment.subject_id == subject_id).all()


def get_assignments_by_faculty(db: Session, faculty_id: int) -> List[Assignment]:
    return db.query(Assignment).filter(Assignment.created_by_id == faculty_id).all()


def create_assignment(db: Session, assignment: AssignmentCreate) -> Assignment:
    db_assignment = Assignment(**assignment.model_dump())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def update_assignment(db: Session, assignment_id: int, assignment_update: AssignmentUpdate) -> Assignment | None:
    db_assignment = get_assignment(db, assignment_id)
    if not db_assignment:
        return None
    update_data = assignment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assignment, field, value)
    db_assignment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def delete_assignment(db: Session, assignment_id: int) -> bool:
    db_assignment = get_assignment(db, assignment_id)
    if not db_assignment:
        return False
    db.delete(db_assignment)
    db.commit()
    return True