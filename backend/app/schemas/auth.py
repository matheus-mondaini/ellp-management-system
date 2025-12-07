"""Pydantic models for authentication flows."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .types import RelaxedEmailStr


class LoginRequest(BaseModel):
    email: RelaxedEmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class AuthenticatedUser(BaseModel):
    id: UUID
    email: RelaxedEmailStr
    role: str
    nome_completo: str
    ativo: bool
    ultimo_login: datetime | None = None

    class Config:
        from_attributes = True
