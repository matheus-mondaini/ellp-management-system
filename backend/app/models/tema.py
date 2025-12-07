"""Tema entity representing workshop classifications."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


oficina_tema_table = Table(
    "oficina_temas",
    Base.metadata,
    Column(
        "oficina_id",
        UUID(as_uuid=True),
        ForeignKey("oficinas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tema_id",
        UUID(as_uuid=True),
        ForeignKey("temas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Tema(Base):
    """High-level topic that groups oficinas."""

    __tablename__ = "temas"
    __table_args__ = (UniqueConstraint("nome", name="uq_temas_nome"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text())
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    oficinas: Mapped[list["Oficina"]] = relationship(
        "Oficina",
        secondary=oficina_tema_table,
        back_populates="temas",
    )


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .oficina import Oficina
