"""Services for RF-021 audit logging."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ..models import Auditoria, User


def registrar_evento(
    db: Session,
    *,
    entidade: str,
    acao: str,
    usuario: User | None,
    entidade_id: UUID | None = None,
    descricao: str | None = None,
    detalhes: Any = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> Auditoria:
    evento = Auditoria(
        entidade=entidade,
        entidade_id=entidade_id,
        acao=acao,
        descricao=descricao,
        detalhes=jsonable_encoder(detalhes) if detalhes is not None else None,
        user_id=usuario.id if usuario else None,
        user_email=usuario.email if usuario else None,
        user_role=usuario.role if usuario else None,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def listar_eventos(
    db: Session,
    *,
    entidade: str | None = None,
    acao: str | None = None,
    limit: int = 50,
) -> list[Auditoria]:
    stmt = select(Auditoria).order_by(desc(Auditoria.created_at)).limit(limit)
    if entidade:
        stmt = stmt.where(Auditoria.entidade == entidade)
    if acao:
        stmt = stmt.where(Auditoria.acao == acao)
    return db.scalars(stmt).all()
