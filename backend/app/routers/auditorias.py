"""Audit log endpoints for RF-021."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import Auditoria, User, UserRole
from ..schemas import AuditoriaRead
from ..services import auditoria_service

router = APIRouter(prefix="/auditorias", tags=["auditorias"])
AdminOnly = Depends(require_role([UserRole.ADMIN]))


def _serialize(evento: Auditoria) -> AuditoriaRead:
    return AuditoriaRead(
        id=evento.id,
        entidade=evento.entidade,
        entidade_id=evento.entidade_id,
        acao=evento.acao,
        descricao=evento.descricao,
        detalhes=evento.detalhes,
        user_id=evento.user_id,
        user_email=evento.user_email,
        user_role=evento.user_role,
        ip_address=evento.ip_address,
        user_agent=evento.user_agent,
        created_at=evento.created_at,
    )


@router.get("", response_model=list[AuditoriaRead])
def listar_auditorias(
    entidade: str | None = Query(None, description="Filtra por entidade"),
    acao: str | None = Query(None, description="Filtra por ação"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = AdminOnly,
) -> list[AuditoriaRead]:
    eventos = auditoria_service.listar_eventos(db, entidade=entidade, acao=acao, limit=limit)
    return [_serialize(evento) for evento in eventos]
