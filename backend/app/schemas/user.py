"""Schemas for user-facing payloads."""
from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from .types import RelaxedEmailStr


class BaseUserCreate(BaseModel):
    email: RelaxedEmailStr
    password: str = Field(min_length=8)
    nome_completo: str
    telefone: str | None = None
    data_nascimento: date | None = None


class AlunoCreate(BaseUserCreate):
    responsavel_nome: str
    responsavel_telefone: str
    responsavel_email: RelaxedEmailStr | None = None
    escola: str | None = None
    serie: str | None = None
    endereco_cidade: str | None = None
    endereco_uf: str | None = Field(default=None, max_length=2)


class TutorCreate(BaseUserCreate):
    faculdade: str | None = None
    curso: str | None = None
    semestre: int | None = Field(default=None, ge=1)
    email_educacional: RelaxedEmailStr | None = None
    tipo_vinculo: str | None = None
    carga_horaria_maxima_semanal: int = Field(default=20, ge=1, le=60)


class ProfessorCreate(BaseUserCreate):
    faculdade: str
    departamento: str | None = None
    titulacao: str | None = None
    email_institucional: RelaxedEmailStr | None = None
    coordenador: bool = False


class UserRead(BaseModel):
    id: UUID
    email: RelaxedEmailStr
    role: str
    nome_completo: str
    ativo: bool

    class Config:
        from_attributes = True
