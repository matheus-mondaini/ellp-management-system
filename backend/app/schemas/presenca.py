"""Schemas relacionados às presenças (RF-007)."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .types import RelaxedEmailStr


class PresencaRegistro(BaseModel):
    inscricao_id: UUID
    presente: bool
    numero_aula: int | None = Field(default=None, ge=1)
    justificativa: str | None = None
    observacao_tutor: str | None = None


class PresencaBatchCreate(BaseModel):
    data_aula: date
    registros: list[PresencaRegistro] = Field(default_factory=list)


class PresencaUpdate(BaseModel):
    data_aula: date | None = None
    numero_aula: int | None = Field(default=None, ge=1)
    presente: bool | None = None
    justificativa: str | None = None
    observacao_tutor: str | None = None


class PresencaRead(BaseModel):
    id: UUID
    inscricao_id: UUID
    aluno_id: UUID
    aluno_nome: str
    aluno_email: RelaxedEmailStr
    data_aula: date
    numero_aula: int | None
    presente: bool
    justificativa: str | None
    observacao_tutor: str | None
    registrado_por: UUID | None
    registrado_por_email: RelaxedEmailStr | None
    created_at: datetime