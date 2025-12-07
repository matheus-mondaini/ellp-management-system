"""Schemas for RF-005 (Inscrição de Alunos)."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.inscricao import InscricaoStatus

from .types import RelaxedEmailStr


class InscricaoCreate(BaseModel):
    aluno_id: UUID
    observacoes: str | None = None


class InscricaoRead(BaseModel):
    id: UUID
    aluno_id: UUID
    aluno_nome: str
    aluno_email: RelaxedEmailStr
    oficina_id: UUID
    status: InscricaoStatus
    data_inscricao: datetime
    observacoes: str | None = None

    class Config:
        from_attributes = True
