import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.refresh_token import RefreshToken
from models.user import User
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from repositories.token import get_refresh_token
from schemas.DTO import RefreshResult
from schemas.user import UserRole
from core.config import REFRESH_EXPIRE_DAYS


class AuthError(Exception):
    pass


class InvalidCredentials(AuthError):
    pass


def create_user(db: Session, username: str, password: str) -> User:
    stmt = select(User).where(User.username == username)
    existing: User | None = db.execute(stmt).scalar_one_or_none()

    if existing:
        raise ValueError("User already exists")

    user = User(username=username, hashed_password=hash_password(password))

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, username: str, password: str) -> User:
    stmt = select(User).where(User.username == username)
    user: User | None = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise InvalidCredentials("Invalid username or password")

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentials("Invalid username or password")

    return user


def create_admin(db: Session, username: str, password: str) -> User:
    stmt = select(User).where(User.username == username)
    existing: User | None = db.execute(stmt).scalar_one_or_none()

    if existing:
        raise ValueError("User already exists")

    user = User(
        username=username, hashed_password=hash_password(password), role=UserRole.ADMIN
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_refresh_token(user_id: int) -> RefreshToken:
    now = datetime.now(timezone.utc)

    refresh_token = RefreshToken(
        token=uuid.uuid4(),
        user_id=user_id,
        expires_at=now + timedelta(days=REFRESH_EXPIRE_DAYS),
    )

    return refresh_token


def refresh_tokens(old_token: str, db: Session) -> RefreshResult:
    now = datetime.now(timezone.utc)

    try:
        token_uuid = uuid.UUID(old_token)
    except ValueError:
        raise HTTPException(401, "Invalid refresh token")

    token = db.execute(
        select(RefreshToken).where(RefreshToken.token == token_uuid)
    ).scalar_one_or_none()

    if not token:
        raise HTTPException(401, "Invalid refresh token")

    if token.expires_at < now:
        db.delete(token)
        db.commit()
        raise HTTPException(401, "Expired refresh token")

    user_id: int = token.user_id

    db.delete(token)

    new_refresh = create_refresh_token(user_id)
    db.add(new_refresh)

    new_access: str = create_access_token({"sub": str(user_id)})

    db.commit()

    return new_access, new_refresh.token


def logout_user(token_value: str | None, db: Session) -> None:
    if not token_value:
        return

    token: RefreshToken | None = get_refresh_token(token_value, db)

    if token:
        db.delete(token)
        db.commit()
