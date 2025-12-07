"""Oficina entity and supporting status enum."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .tema import oficina_tema_table


oficina_tutor_table = Table(
    "oficina_tutores",
    Base.metadata,
    Column(
        "oficina_id",
        UUID(as_uuid=True),
        ForeignKey("oficinas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tutor_id",
        UUID(as_uuid=True),
        ForeignKey("tutores.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    UniqueConstraint("oficina_id", "tutor_id", name="uq_oficina_tutor_unique"),
)

class OficinaStatus(StrEnum):
    """Lifecycle status options for workshops."""

    PLANEJADA = "planejada"
    INSCRICOES_ABERTAS = "inscricoes_abertas"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class Oficina(Base):
    __tablename__ = "oficinas"
    __table_args__ = (
        CheckConstraint("capacidade_maxima >= 1", name="ck_oficinas_capacidade"),
        CheckConstraint("carga_horaria >= 1", name="ck_oficinas_carga_horaria"),
        CheckConstraint("data_fim >= data_inicio", name="ck_oficinas_periodo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    professor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professores.id", ondelete="RESTRICT"),
        nullable=False,
    )
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text())
    carga_horaria: Mapped[int] = mapped_column(Integer, nullable=False)
    capacidade_maxima: Mapped[int] = mapped_column(Integer, nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date(), nullable=False)
    data_fim: Mapped[date] = mapped_column(Date(), nullable=False)
    local: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[OficinaStatus] = mapped_column(
        Enum(OficinaStatus, native_enum=False),
        default=OficinaStatus.PLANEJADA,
        nullable=False,
    )
    observacoes: Mapped[str | None] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    professor: Mapped["Professor"] = relationship("Professor", back_populates="oficinas")
    temas: Mapped[list["Tema"]] = relationship(
        "Tema",
        secondary=oficina_tema_table,
        back_populates="oficinas",
    )
    tutores: Mapped[list["Tutor"]] = relationship(
        "Tutor",
        secondary=oficina_tutor_table,
        back_populates="oficinas",
    )
    inscricoes: Mapped[list["Inscricao"]] = relationship(
        "Inscricao",
        back_populates="oficina",
        cascade="all, delete-orphan",
    )


if TYPE_CHECKING:  # pragma: no cover
    from .professor import Professor
    from .tema import Tema
    from .tutor import Tutor
    from .inscricao import Inscricao
