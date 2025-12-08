"""Schemas for RF-021 audit events."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AuditoriaRead(BaseModel):
    id: UUID
    entidade: str
    entidade_id: UUID | None
    acao: str
    descricao: str | None = None
    detalhes: dict | None = None
    user_id: UUID | None = None
    user_email: str | None = None
    user_role: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
