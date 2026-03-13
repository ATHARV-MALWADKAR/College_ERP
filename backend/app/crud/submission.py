from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.db.models.submission import Submission
from app.schemas.submission import SubmissionCreate, SubmissionUpdate


def get_submission(db: Session, submission_id: int) -> Submission | None:
    return db.query(Submission).filter(Submission.id == submission_id).first()


def get_submissions_by_assignment(db: Session, assignment_id: int) -> List[Submission]:
    return db.query(Submission).filter(Submission.assignment_id == assignment_id).all()


def get_submission_by_student_assignment(db: Session, student_id: int, assignment_id: int) -> Submission | None:
    return db.query(Submission).filter(
        Submission.student_id == student_id,
        Submission.assignment_id == assignment_id
    ).first()


def get_submissions_by_student(db: Session, student_id: int) -> List[Submission]:
    return db.query(Submission).filter(Submission.student_id == student_id).all()


def create_submission(db: Session, submission: SubmissionCreate, file_path: str | None = None) -> Submission:
    db_submission = Submission(
        **submission.model_dump(),
        submitted_at=datetime.utcnow(),
        file_path=file_path
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def update_submission(db: Session, submission_id: int, submission_update: SubmissionUpdate) -> Submission | None:
    db_submission = get_submission(db, submission_id)
    if not db_submission:
        return None
    update_data = submission_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_submission, field, value)
    db_submission.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_submission)
    return db_submission


def delete_submission(db: Session, submission_id: int) -> bool:
    db_submission = get_submission(db, submission_id)
    if not db_submission:
        return False
    db.delete(db_submission)
    db.commit()
    return True