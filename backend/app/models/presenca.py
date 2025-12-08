"""Registro de presença por sessão de oficina."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Presenca(Base):
    __tablename__ = "presencas"
    __table_args__ = (
        UniqueConstraint("inscricao_id", "data_aula", name="uq_presenca_inscricao_data"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inscricao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("inscricoes.id", ondelete="CASCADE"), nullable=False
    )
    data_aula: Mapped[date] = mapped_column(Date(), nullable=False)
    numero_aula: Mapped[int | None] = mapped_column(Integer)
    presente: Mapped[bool] = mapped_column(Boolean, nullable=False)
    justificativa: Mapped[str | None] = mapped_column(Text())
    observacao_tutor: Mapped[str | None] = mapped_column(Text())
    registrado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    inscricao: Mapped["Inscricao"] = relationship("Inscricao", back_populates="presencas")
    registrado_por_user: Mapped["User | None"] = relationship("User")


if TYPE_CHECKING:  # pragma: no cover
    from .inscricao import Inscricao
    from .user import User
