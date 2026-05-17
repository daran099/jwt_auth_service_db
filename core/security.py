from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from core.dependencies import get_db
from models.user import User
from schemas.user import UserRole

pwd_context: CryptContext = CryptContext(schemes=["argon2"], deprecated="auto")

security: HTTPBearer = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode: dict = data.copy()

    expire: datetime = datetime.now(timezone.utc) + timedelta(
        ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire, "type": "access"})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token: str = credentials.credentials

    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = int(payload["sub"])

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    stmt = select(User).where(User.id == user_id)
    user: User | None = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return user
