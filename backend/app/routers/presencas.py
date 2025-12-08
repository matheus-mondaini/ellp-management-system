"""Endpoints para registro e listagem de presenças (RF-007)."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import User, UserRole
from ..schemas import PresencaBatchCreate, PresencaRead, PresencaUpdate
from ..services import presenca_service

router = APIRouter(prefix="/presencas", tags=["presencas"])

TutorOrHigher = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR, UserRole.TUTOR]))


def _serialize_presenca(entry) -> PresencaRead:
    inscricao = entry.inscricao
    aluno = inscricao.aluno
    pessoa = aluno.pessoa
    usuario = pessoa.user
    registrador_email = entry.registrado_por_user.email if entry.registrado_por_user else None
    return PresencaRead(
        id=entry.id,
        inscricao_id=entry.inscricao_id,
        aluno_id=aluno.id,
        aluno_nome=pessoa.nome_completo,
        aluno_email=usuario.email,
        data_aula=entry.data_aula,
        numero_aula=entry.numero_aula,
        presente=entry.presente,
        justificativa=entry.justificativa,
        observacao_tutor=entry.observacao_tutor,
        registrado_por=entry.registrado_por_id,
        registrado_por_email=registrador_email,
        created_at=entry.created_at,
    )


@router.get("/oficinas/{oficina_id}", response_model=list[PresencaRead])
def list_presencas_oficina(
    oficina_id: UUID,
    data_aula: date | None = None,
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> list[PresencaRead]:
    presencas = presenca_service.list_by_oficina(db, oficina_id, data_aula=data_aula)
    return [_serialize_presenca(item) for item in presencas]


@router.get("/inscricoes/{inscricao_id}", response_model=list[PresencaRead])
def list_presencas_inscricao(
    inscricao_id: UUID,
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> list[PresencaRead]:
    presencas = presenca_service.list_by_inscricao(db, inscricao_id)
    return [_serialize_presenca(item) for item in presencas]


@router.post(
    "/oficinas/{oficina_id}",
    response_model=list[PresencaRead],
    status_code=status.HTTP_201_CREATED,
)
def registrar_presencas(
    oficina_id: UUID,
    payload: PresencaBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = TutorOrHigher,
) -> list[PresencaRead]:
    presencas = presenca_service.registrar_lote(
        db,
        oficina_id,
        data_aula=payload.data_aula,
        registros=payload.registros,
        registrador_id=current_user.id,
    )
    return [_serialize_presenca(item) for item in presencas]


@router.patch("/{presenca_id}", response_model=PresencaRead)
def atualizar_presenca(
    presenca_id: UUID,
    payload: PresencaUpdate,
    db: Session = Depends(get_db),
    current_user: User = TutorOrHigher,
) -> PresencaRead:
    presenca = presenca_service.update_presenca(
        db,
        presenca_id,
        payload,
        registrador_id=current_user.id,
    )
    return _serialize_presenca(presenca)


@router.delete("/{presenca_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_presenca(
    presenca_id: UUID,
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> Response:
    presenca_service.delete_presenca(db, presenca_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
