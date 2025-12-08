"""Schemas for RF-021 audit events."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AuditoriaRead(BaseModel):
    id: UUID
    recurso: str
    recurso_id: UUID | None
    acao: str
    descricao: str | None = None
    payload: dict | None = None
    usuario_id: UUID | None = None
    usuario_email: str | None = None
    criado_em: datetime

    class Config:
        from_attributes = True
