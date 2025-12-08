"""Endpoints for managing oficinas (RF-003/RF-004)."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import User, UserRole
from ..models.oficina import OficinaStatus
from ..schemas import (
    InscricaoCreate,
    InscricaoRead,
    OficinaCreate,
    OficinaRead,
    OficinaUpdate,
    TutorAssignmentRead,
)
from ..services import auditoria_service, inscricao_service, oficina_service
from ._serializers import serialize_inscricao

router = APIRouter(prefix="/oficinas", tags=["oficinas"])

AdminOrProfessor = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR]))
TutorOrHigher = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR, UserRole.TUTOR]))
AdminOnly = Depends(require_role([UserRole.ADMIN]))


@router.get("", response_model=list[OficinaRead])
def list_oficinas(
    status: OficinaStatus | None = None,
    tema_id: UUID | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    db: Session = Depends(get_db),
    _: None = TutorOrHigher,
) -> list[OficinaRead]:
    return oficina_service.list_oficinas(
        db,
        status_filter=status,
        tema_id=tema_id,
        start_date=data_inicio,
        end_date=data_fim,
    )


@router.post("", response_model=OficinaRead, status_code=status.HTTP_201_CREATED)
def create_oficina(
    payload: OficinaCreate,
    db: Session = Depends(get_db),
    current_user: User = AdminOrProfessor,
) -> OficinaRead:
    oficina = oficina_service.create_oficina(db, payload)
    auditoria_service.registrar_evento(
        db,
        entidade="oficina",
        entidade_id=oficina.id,
        acao="criada",
        usuario=current_user,
        detalhes=payload.model_dump(),
    )
    return oficina


@router.get("/{oficina_id}", response_model=OficinaRead)
def retrieve_oficina(
    oficina_id: UUID,
    db: Session = Depends(get_db),
    _: None = AdminOrProfessor,
) -> OficinaRead:
    return oficina_service.get_oficina(db, oficina_id)


@router.patch("/{oficina_id}", response_model=OficinaRead)
def update_oficina(
    oficina_id: UUID,
    payload: OficinaUpdate,
    db: Session = Depends(get_db),
    current_user: User = AdminOrProfessor,
) -> OficinaRead:
    oficina = oficina_service.update_oficina(db, oficina_id, payload)
    auditoria_service.registrar_evento(
        db,
        entidade="oficina",
        entidade_id=oficina.id,
        acao="atualizada",
        usuario=current_user,
        detalhes=payload.model_dump(exclude_unset=True),
    )
    return oficina


@router.delete("/{oficina_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_oficina(
    oficina_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOrProfessor,
) -> Response:
    oficina_service.delete_oficina(db, oficina_id)
    auditoria_service.registrar_evento(
        db,
        entidade="oficina",
        entidade_id=oficina_id,
        acao="removida",
        usuario=current_user,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _serialize_tutor_assignment(tutor) -> TutorAssignmentRead:
    pessoa = tutor.pessoa
    return TutorAssignmentRead(
        tutor_id=tutor.id,
        nome=pessoa.nome_completo,
        email=pessoa.user.email,
        carga_horaria_maxima_semanal=tutor.carga_horaria_maxima_semanal,
        carga_horaria_alocada=float(tutor.carga_horaria_atual or 0),
    )


@router.get("/{oficina_id}/tutores", response_model=list[TutorAssignmentRead])
def list_oficina_tutores(
    oficina_id: UUID,
    db: Session = Depends(get_db),
    _: None = AdminOrProfessor,
) -> list[TutorAssignmentRead]:
    tutores = oficina_service.list_oficina_tutores(db, oficina_id)
    return [_serialize_tutor_assignment(tutor) for tutor in tutores]


@router.post(
    "/{oficina_id}/tutores/{tutor_id}",
    response_model=TutorAssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
def assign_tutor(
    oficina_id: UUID,
    tutor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOrProfessor,
) -> TutorAssignmentRead:
    tutor = oficina_service.assign_tutor_to_oficina(db, oficina_id, tutor_id)
    auditoria_service.registrar_evento(
        db,
        entidade="oficina_tutor",
        entidade_id=oficina_id,
        acao="associado",
        usuario=current_user,
        detalhes={"tutor_id": str(tutor_id)},
    )
    return _serialize_tutor_assignment(tutor)


@router.delete("/{oficina_id}/tutores/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tutor(
    oficina_id: UUID,
    tutor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOrProfessor,
) -> Response:
    oficina_service.remove_tutor_from_oficina(db, oficina_id, tutor_id)
    auditoria_service.registrar_evento(
        db,
        entidade="oficina_tutor",
        entidade_id=oficina_id,
        acao="removido",
        usuario=current_user,
        detalhes={"tutor_id": str(tutor_id)},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{oficina_id}/professor/{professor_id}", response_model=OficinaRead)
def set_responsavel_professor(
    oficina_id: UUID,
    professor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOnly,
) -> OficinaRead:
    oficina = oficina_service.update_oficina_professor(db, oficina_id, professor_id)
    auditoria_service.registrar_evento(
        db,
        entidade="oficina",
        entidade_id=oficina_id,
        acao="responsavel_atualizado",
        usuario=current_user,
        detalhes={"professor_id": str(professor_id)},
    )
    return oficina


@router.get("/{oficina_id}/inscricoes", response_model=list[InscricaoRead])
def list_oficina_inscricoes(
    oficina_id: UUID,
    db: Session = Depends(get_db),
    _: None = TutorOrHigher,
) -> list[InscricaoRead]:
    inscricoes = inscricao_service.list_inscricoes(db, oficina_id)
    return [serialize_inscricao(item) for item in inscricoes]


@router.post(
    "/{oficina_id}/inscricoes",
    response_model=InscricaoRead,
    status_code=status.HTTP_201_CREATED,
)
def create_oficina_inscricao(
    oficina_id: UUID,
    payload: InscricaoCreate,
    db: Session = Depends(get_db),
    current_user: User = TutorOrHigher,
) -> InscricaoRead:
    inscricao = inscricao_service.create_inscricao(db, oficina_id, payload)
    auditoria_service.registrar_evento(
        db,
        entidade="inscricao",
        entidade_id=inscricao.id,
        acao="criada",
        usuario=current_user,
        detalhes={"oficina_id": str(oficina_id), "aluno_id": str(payload.aluno_id)},
    )
    return serialize_inscricao(inscricao)
