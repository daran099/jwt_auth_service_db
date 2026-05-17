from sqlalchemy import select
from sqlalchemy.orm import Session

from models.refresh_token import RefreshToken
from models.user import User


def get_refresh_token(token: str, db: Session) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.token == token)

    result = db.execute(stmt)

    return result.scalar_one_or_none()


def delete_refresh_token(token: RefreshToken, db: Session) -> None:
    db.delete(token)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)

    return db.execute(stmt).scalar_one_or_none()


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)

    return db.execute(stmt).scalar_one_or_none()
