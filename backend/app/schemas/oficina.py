"""Pydantic models for Oficina resources."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.oficina import OficinaStatus

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


class OficinaRead(OficinaBase):
    id: UUID
    professor_id: UUID
    temas: list[TemaRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
