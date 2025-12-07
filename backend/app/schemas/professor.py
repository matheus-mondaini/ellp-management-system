"""Pydantic models for professor management."""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from .oficina import OficinaSummary
from .types import RelaxedEmailStr


class ProfessorRead(BaseModel):
    id: UUID
    nome: str
    email: RelaxedEmailStr
    faculdade: str
    departamento: str | None = None
    coordenador: bool = False


class ProfessorDetailRead(ProfessorRead):
    area_atuacao: str | None = None
    observacoes: str | None = None
    oficinas: list[OficinaSummary] = Field(default_factory=list)