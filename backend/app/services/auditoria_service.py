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
    recurso: str,
    recurso_id: UUID | None,
    acao: str,
    usuario: User | None,
    descricao: str | None = None,
    payload: Any = None,
) -> Auditoria:
    evento = Auditoria(
        recurso=recurso,
        recurso_id=recurso_id,
        acao=acao,
        usuario_id=usuario.id if usuario else None,
        descricao=descricao,
        payload=jsonable_encoder(payload) if payload is not None else None,
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def listar_eventos(
    db: Session,
    *,
    recurso: str | None = None,
    acao: str | None = None,
    limit: int = 50,
) -> list[Auditoria]:
    stmt = select(Auditoria).order_by(desc(Auditoria.criado_em)).limit(limit)
    if recurso:
        stmt = stmt.where(Auditoria.recurso == recurso)
    if acao:
        stmt = stmt.where(Auditoria.acao == acao)
    return db.scalars(stmt).all()
