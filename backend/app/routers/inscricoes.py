"""Endpoints para gestão de progresso das inscrições (RF-031/RF-032)."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import User, UserRole
from ..schemas import InscricaoRead, InscricaoStatusUpdate
from ..services import inscricao_service
from ._serializers import serialize_inscricao

router = APIRouter(prefix="/inscricoes", tags=["inscricoes"])
TutorOrHigher = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR, UserRole.TUTOR]))


@router.patch("/{inscricao_id}/status", response_model=InscricaoRead)
def atualizar_status(
    inscricao_id: UUID,
    payload: InscricaoStatusUpdate,
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> InscricaoRead:
    inscricao_service.update_status(db, inscricao_id, payload.status)
    atualizado = inscricao_service.get_inscricao(db, inscricao_id)
    return serialize_inscricao(atualizado)
