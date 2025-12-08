"""Endpoints para RF-013 (Histórico de Participação)."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import User, UserRole
from ..schemas import HistoricoParticipacaoRead
from ..services import historico_service

router = APIRouter(prefix="/historicos", tags=["historicos"])
AdminOrAluno = Depends(require_role([UserRole.ADMIN, UserRole.ALUNO]))
AdminOrTutor = Depends(require_role([UserRole.ADMIN, UserRole.TUTOR]))
AdminOrProfessor = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR]))


def _assert_self_or_admin(current_user: User, attr_name: str, entity_id: UUID) -> None:
    if current_user.role == UserRole.ADMIN:
        return
    pessoa = current_user.pessoa
    entidade = getattr(pessoa, attr_name, None) if pessoa else None
    if not entidade or entidade.id != entity_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para consultar este histórico",
        )


@router.get("/alunos/{aluno_id}", response_model=HistoricoParticipacaoRead)
def historico_alunos(
    aluno_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOrAluno,
) -> HistoricoParticipacaoRead:
    _assert_self_or_admin(current_user, "aluno", aluno_id)
    payload = historico_service.historico_aluno(db, aluno_id)
    return HistoricoParticipacaoRead(**payload)


@router.get("/tutores/{tutor_id}", response_model=HistoricoParticipacaoRead)
def historico_tutores(
    tutor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOrTutor,
) -> HistoricoParticipacaoRead:
    _assert_self_or_admin(current_user, "tutor", tutor_id)
    payload = historico_service.historico_tutor(db, tutor_id)
    return HistoricoParticipacaoRead(**payload)


@router.get("/professores/{professor_id}", response_model=HistoricoParticipacaoRead)
def historico_professores(
    professor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOrProfessor,
) -> HistoricoParticipacaoRead:
    _assert_self_or_admin(current_user, "professor", professor_id)
    payload = historico_service.historico_professor(db, professor_id)
    return HistoricoParticipacaoRead(**payload)
