from sqlalchemy.orm import Session, joinedload

from app.core.security import hash_password
from app.db.models import Role, User


def get_role_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.id == user_id)
        .first()
    )


def create_user(
    db: Session,
    email: str,
    full_name: str,
    password: str,
    role_name: str,
) -> User:
    role = get_role_by_name(db, role_name)
    if not role:
        raise ValueError(f"Unknown role: {role_name}")
    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hash_password(password),
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
