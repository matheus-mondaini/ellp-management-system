"""Pydantic models for Oficina resources."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.oficina import OficinaStatus

from .types import RelaxedEmailStr
from .tema import TemaRead


class OficinaBase(BaseModel):
    titulo: str
    descricao: str | None = None
    carga_horaria: int = Field(gt=0)
    capacidade_maxima: int = Field(gt=0)
    data_inicio: date
    data_fim: date
    local: str
    status: OficinaStatus = OficinaStatus.PLANEJADA


class OficinaCreate(OficinaBase):
    professor_id: UUID
    tema_ids: list[UUID] = Field(default_factory=list)


class OficinaUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    carga_horaria: int | None = Field(default=None, gt=0)
    capacidade_maxima: int | None = Field(default=None, gt=0)
    data_inicio: date | None = None
    data_fim: date | None = None
    local: str | None = None
    status: OficinaStatus | None = None
    professor_id: UUID | None = None
    tema_ids: list[UUID] | None = None


class OficinaRead(OficinaBase):
    id: UUID
    professor_id: UUID
    temas: list[TemaRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TutorAssignmentRead(BaseModel):
    tutor_id: UUID
    nome: str
    email: RelaxedEmailStr
    carga_horaria_maxima_semanal: int
    carga_horaria_alocada: float


class OficinaSummary(BaseModel):
    id: UUID
    titulo: str
    status: OficinaStatus
    data_inicio: date
    data_fim: date

    class Config:
        from_attributes = True

