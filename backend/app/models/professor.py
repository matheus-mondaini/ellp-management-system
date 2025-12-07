"""Professor entity."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Professor(Base):
    __tablename__ = "professores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pessoa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pessoas.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    faculdade: Mapped[str] = mapped_column(String(255))
    departamento: Mapped[str | None] = mapped_column(String(255))
    titulacao: Mapped[str | None] = mapped_column(String(100))
    email_institucional: Mapped[str | None] = mapped_column(String(255))
    segundo_email: Mapped[str | None] = mapped_column(String(255))
    coordenador: Mapped[bool] = mapped_column(Boolean, default=False)
    area_atuacao: Mapped[str | None] = mapped_column(String(255))
    observacoes: Mapped[str | None] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    pessoa: Mapped["Pessoa"] = relationship(back_populates="professor")


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .pessoa import Pessoa
