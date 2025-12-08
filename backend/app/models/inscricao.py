"""Inscricao entity linking alunos and oficinas."""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class InscricaoStatus(StrEnum):
    """Valid lifecycle stages for an enrollment."""

    INSCRITO = "inscrito"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"
    ABANDONOU = "abandonou"
    CANCELADO = "cancelado"


class Inscricao(Base):
    __tablename__ = "inscricoes"
    __table_args__ = (
        UniqueConstraint("aluno_id", "oficina_id", name="uq_inscricao_aluno_oficina"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    aluno_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False
    )
    oficina_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("oficinas.id", ondelete="CASCADE"), nullable=False
    )

    data_inscricao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    status: Mapped[InscricaoStatus] = mapped_column(
        Enum(InscricaoStatus, native_enum=False),
        default=InscricaoStatus.INSCRITO,
        nullable=False,
    )
    percentual_presenca: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    total_aulas_previstas: Mapped[int] = mapped_column(default=0)
    total_presencas: Mapped[int] = mapped_column(default=0)
    total_faltas: Mapped[int] = mapped_column(default=0)
    apto_certificado: Mapped[bool] = mapped_column(Boolean, default=False)
    data_conclusao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    observacoes: Mapped[str | None] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    aluno: Mapped["Aluno"] = relationship("Aluno", back_populates="inscricoes")
    oficina: Mapped["Oficina"] = relationship("Oficina", back_populates="inscricoes")
    presencas: Mapped[list["Presenca"]] = relationship(
        "Presenca",
        back_populates="inscricao",
        cascade="all, delete-orphan",
    )


if TYPE_CHECKING:  # pragma: no cover
    from .aluno import Aluno
    from .oficina import Oficina
    from .presenca import Presenca
