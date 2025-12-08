"""Certificado entity for RF-008/033."""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CertificadoTipo(StrEnum):
    """Supported certificate variants."""

    CONCLUSAO_ALUNO = "conclusao_aluno"
    PARTICIPACAO_TUTOR = "participacao_tutor"


class Certificado(Base):
    __tablename__ = "certificados"
    __table_args__ = (
        UniqueConstraint("inscricao_id", name="uq_certificados_inscricao"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inscricao_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("inscricoes.id", ondelete="SET NULL"), nullable=True
    )
    tutor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tutores.id", ondelete="SET NULL"), nullable=True
    )
    oficina_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("oficinas.id", ondelete="SET NULL"), nullable=False
    )
    tipo: Mapped[CertificadoTipo] = mapped_column(Enum(CertificadoTipo, native_enum=False), nullable=False)

    hash_validacao: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    codigo_verificacao: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    arquivo_pdf_url: Mapped[str | None] = mapped_column(Text())
    arquivo_pdf_nome: Mapped[str | None] = mapped_column(String(255))

    data_emissao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    valido_ate: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    carga_horaria_certificada: Mapped[int | None] = mapped_column(Integer)
    percentual_presenca_certificado: Mapped[float | None] = mapped_column(Numeric(5, 2))

    revogado: Mapped[bool] = mapped_column(Boolean, default=False)
    data_revogacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    motivo_revogacao: Mapped[str | None] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    inscricao: Mapped["Inscricao | None"] = relationship("Inscricao", back_populates="certificado")
    tutor: Mapped["Tutor | None"] = relationship("Tutor")
    oficina: Mapped["Oficina"] = relationship("Oficina")


if TYPE_CHECKING:  # pragma: no cover
    from .inscricao import Inscricao
    from .oficina import Oficina
    from .tutor import Tutor
