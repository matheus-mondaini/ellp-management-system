"""Tutor entity."""
from __future__ import annotations

import uuid
from datetime import datetime, date

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Tutor(Base):
    __tablename__ = "tutores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pessoa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pessoas.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    faculdade: Mapped[str | None] = mapped_column(String(255))
    curso: Mapped[str | None] = mapped_column(String(255))
    semestre: Mapped[int | None] = mapped_column(Integer)
    ra: Mapped[str | None] = mapped_column(String(50))
    email_educacional: Mapped[str | None] = mapped_column(String(255))

    profissao: Mapped[str | None] = mapped_column(String(255))
    empresa: Mapped[str | None] = mapped_column(String(255))
    linkedin: Mapped[str | None] = mapped_column(String(255))

    tipo_vinculo: Mapped[str | None] = mapped_column(String(50))
    data_inicio_voluntariado: Mapped[date | None] = mapped_column(Date())
    data_fim_voluntariado: Mapped[date | None] = mapped_column(Date())
    status_voluntariado: Mapped[str] = mapped_column(String(50), default="Ativo")

    carga_horaria_maxima_semanal: Mapped[int] = mapped_column(default=20)
    carga_horaria_atual: Mapped[float] = mapped_column(Numeric(5, 2), default=0)

    areas_interesse: Mapped[str | None] = mapped_column(Text())
    observacoes: Mapped[str | None] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    pessoa: Mapped["Pessoa"] = relationship(back_populates="tutor")


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .pessoa import Pessoa
