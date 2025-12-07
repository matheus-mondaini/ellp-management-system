"""Aluno entity."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pessoa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pessoas.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    endereco_rua: Mapped[str | None] = mapped_column(String(255))
    endereco_numero: Mapped[str | None] = mapped_column(String(10))
    endereco_complemento: Mapped[str | None] = mapped_column(String(100))
    endereco_bairro: Mapped[str | None] = mapped_column(String(100))
    endereco_cidade: Mapped[str | None] = mapped_column(String(100))
    endereco_uf: Mapped[str | None] = mapped_column(String(2))
    endereco_cep: Mapped[str | None] = mapped_column(String(10))

    escola: Mapped[str | None] = mapped_column(String(255))
    serie: Mapped[str | None] = mapped_column(String(50))
    turno: Mapped[str | None] = mapped_column(String(20))

    responsavel_nome: Mapped[str] = mapped_column(String(255))
    responsavel_cpf: Mapped[str | None] = mapped_column(String(14))
    responsavel_email: Mapped[str | None] = mapped_column(String(255))
    responsavel_telefone: Mapped[str] = mapped_column(String(20))
    responsavel_parentesco: Mapped[str | None] = mapped_column(String(50))
    responsavel_profissao: Mapped[str | None] = mapped_column(String(100))

    observacoes: Mapped[str | None] = mapped_column(Text())
    necessidades_especiais: Mapped[str | None] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    pessoa: Mapped["Pessoa"] = relationship(back_populates="aluno")
    inscricoes: Mapped[list["Inscricao"]] = relationship(
        "Inscricao",
        back_populates="aluno",
        cascade="all, delete-orphan",
    )


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .pessoa import Pessoa
    from .inscricao import Inscricao
