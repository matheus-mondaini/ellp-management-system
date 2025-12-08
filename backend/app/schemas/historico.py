"""Participation history schemas for RF-013."""
from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class HistoricoParticipacaoItem(BaseModel):
    oficina_id: UUID
    oficina_titulo: str
    papel: Literal["aluno", "tutor", "professor"]
    status_oficina: str
    data_inicio: date
    data_fim: date
    carga_horaria: int
    status_inscricao: str | None = None
    percentual_presenca: float | None = Field(default=None, ge=0)
    certificado_emitido: bool | None = None


class HistoricoParticipacaoRead(BaseModel):
    referencia_tipo: Literal["aluno", "tutor", "professor"]
    referencia_id: UUID
    total_registros: int
    itens: list[HistoricoParticipacaoItem]
