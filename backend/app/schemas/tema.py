"""Pydantic models for Tema resources."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TemaBase(BaseModel):
    nome: str
    descricao: str | None = None
    ativo: bool = True


class TemaCreate(TemaBase):
    pass


class TemaRead(TemaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
