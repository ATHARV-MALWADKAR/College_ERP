from sqlalchemy.orm import Session

from app.db.models import Student


def list_students(db: Session) -> list[Student]:
    return (
        db.query(Student)
        .order_by(Student.created_at.desc())
        .all()
    )


def get_student(db: Session, student_id: int) -> Student | None:
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(
    db: Session,
    *,
    user_id: int,
    roll_number: str,
    department_id: int,
    course_id: int,
    batch: str,
) -> Student:
    student = Student(
        user_id=user_id,
        roll_number=roll_number,
        department_id=department_id,
        course_id=course_id,
        batch=batch,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(
    db: Session,
    *,
    student_id: int,
    roll_number: str | None = None,
    department_id: int | None = None,
    course_id: int | None = None,
    batch: str | None = None,
) -> Student | None:
    student = get_student(db, student_id)
    if not student:
        return None
    if roll_number is not None:
        student.roll_number = roll_number
    if department_id is not None:
        student.department_id = department_id
    if course_id is not None:
        student.course_id = course_id
    if batch is not None:
        student.batch = batch
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int) -> bool:
    student = get_student(db, student_id)
    if not student:
        return False
    db.delete(student)
    db.commit()
    return True

