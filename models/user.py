from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from db.base import Base
from schemas.user import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role_enum"), default=UserRole.USER, nullable=False
    )

    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
