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
    usuario_email = evento.usuario.email if evento.usuario else None
    return AuditoriaRead(
        id=evento.id,
        recurso=evento.recurso,
        recurso_id=evento.recurso_id,
        acao=evento.acao,
        descricao=evento.descricao,
        payload=evento.payload,
        usuario_id=evento.usuario_id,
        usuario_email=usuario_email,
        criado_em=evento.criado_em,
    )


@router.get("", response_model=list[AuditoriaRead])
def listar_auditorias(
    recurso: str | None = Query(None, description="Filtra por recurso"),
    acao: str | None = Query(None, description="Filtra por ação"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = AdminOnly,
) -> list[AuditoriaRead]:
    eventos = auditoria_service.listar_eventos(db, recurso=recurso, acao=acao, limit=limit)
    return [_serialize(evento) for evento in eventos]
