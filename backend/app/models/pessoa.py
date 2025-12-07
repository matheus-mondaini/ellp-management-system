"""Common personal data shared by every profile."""
from __future__ import annotations

import uuid
from datetime import datetime, date

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Pessoa(Base):
    __tablename__ = "pessoas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    nome_completo: Mapped[str] = mapped_column(String(255), nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20))
    data_nascimento: Mapped[date | None] = mapped_column(Date())
    foto_url: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="pessoa")
    aluno: Mapped["Aluno | None"] = relationship(
        back_populates="pessoa", cascade="all, delete-orphan"
    )
    tutor: Mapped["Tutor | None"] = relationship(
        back_populates="pessoa", cascade="all, delete-orphan"
    )
    professor: Mapped["Professor | None"] = relationship(
        back_populates="pessoa", cascade="all, delete-orphan"
    )


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import-time cycle guards
    from .user import User
    from .aluno import Aluno
    from .tutor import Tutor
    from .professor import Professor
