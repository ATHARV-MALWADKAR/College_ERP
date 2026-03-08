from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.crud.user import get_user_by_id
from app.db.models import User
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Require valid JWT and return current user."""
    payload = decode_access_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_id(db, int(payload["user_id"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_active_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require current user to be active."""
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


def require_roles(*allowed_roles: str):
    """Dependency factory: restrict access to given role names (e.g. 'admin', 'faculty')."""

    def _require_roles(
        user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        role_name = user.role.name if user.role else None
        if role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: one of {list(allowed_roles)}",
            )
        return user

    return _require_roles


# Typed dependencies for route signatures
CurrentUser = Annotated[User, Depends(get_current_active_user)]

RequireStudent = Annotated[User, Depends(require_roles("student"))]
RequireFaculty = Annotated[User, Depends(require_roles("faculty"))]
RequireAdmin = Annotated[User, Depends(require_roles("admin"))]
