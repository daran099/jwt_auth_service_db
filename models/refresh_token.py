from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from sqlalchemy.dialects.postgresql import UUID


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    token: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    user: Mapped[User] = relationship(back_populates="refresh_tokens")
