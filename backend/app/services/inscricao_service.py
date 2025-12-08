"""Business rules for RF-005/RF-031/RF-032 (Inscrições e progresso)."""
from __future__ import annotations

from datetime import date, datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from ..models import Aluno, Inscricao, Oficina, Pessoa
from ..models.inscricao import InscricaoStatus
from ..models.oficina import OficinaStatus
from ..schemas import InscricaoCreate

INSCRICAO_WITH_USER = (
    selectinload(Inscricao.aluno)
    .selectinload(Aluno.pessoa)
    .selectinload(Pessoa.user)
)

ALLOWED_TRANSITIONS: dict[InscricaoStatus, set[InscricaoStatus]] = {
    InscricaoStatus.INSCRITO: {
        InscricaoStatus.EM_ANDAMENTO,
        InscricaoStatus.CANCELADO,
        InscricaoStatus.ABANDONOU,
    },
    InscricaoStatus.EM_ANDAMENTO: {
        InscricaoStatus.CONCLUIDO,
        InscricaoStatus.CANCELADO,
        InscricaoStatus.ABANDONOU,
    },
    InscricaoStatus.CONCLUIDO: set(),
    InscricaoStatus.CANCELADO: set(),
    InscricaoStatus.ABANDONOU: set(),
}


def _get_oficina_or_404(db: Session, oficina_id: UUID) -> Oficina:
    oficina = db.get(Oficina, oficina_id)
    if not oficina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oficina não encontrada")
    return oficina


def _get_aluno_or_404(db: Session, aluno_id: UUID) -> Aluno:
    aluno = db.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    return aluno


def _get_inscricao_or_404(db: Session, inscricao_id: UUID) -> Inscricao:
    inscricao = db.get(Inscricao, inscricao_id)
    if not inscricao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")
    return inscricao


def _validate_oficina_accepts_new_entries(oficina: Oficina) -> None:
    if oficina.status not in (OficinaStatus.PLANEJADA, OficinaStatus.INSCRICOES_ABERTAS):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Oficina não aceita novas inscrições",
        )
    if oficina.data_fim < date.today():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Período encerrado para inscrições",
        )


def _ensure_capacity(db: Session, oficina: Oficina) -> None:
    stmt = select(func.count(Inscricao.id)).where(Inscricao.oficina_id == oficina.id)
    current = db.execute(stmt).scalar_one()
    if current >= oficina.capacidade_maxima:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Capacidade máxima atingida",
        )


def list_inscricoes(db: Session, oficina_id: UUID) -> list[Inscricao]:
    _get_oficina_or_404(db, oficina_id)
    stmt = (
        select(Inscricao)
        .options(INSCRICAO_WITH_USER)
        .where(Inscricao.oficina_id == oficina_id)
        .order_by(Inscricao.created_at.asc())
    )
    return db.scalars(stmt).all()


def create_inscricao(db: Session, oficina_id: UUID, payload: InscricaoCreate) -> Inscricao:
    oficina = _get_oficina_or_404(db, oficina_id)
    aluno = _get_aluno_or_404(db, payload.aluno_id)

    stmt = select(Inscricao.id).where(
        Inscricao.oficina_id == oficina_id,
        Inscricao.aluno_id == payload.aluno_id,
    )
    if db.execute(stmt).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Aluno já inscrito")

    _validate_oficina_accepts_new_entries(oficina)
    _ensure_capacity(db, oficina)

    inscricao = Inscricao(
        aluno=aluno,
        oficina=oficina,
        status=InscricaoStatus.INSCRITO,
        observacoes=payload.observacoes,
    )
    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)
    return inscricao


def get_inscricao(db: Session, inscricao_id: UUID) -> Inscricao:
    stmt = select(Inscricao).options(INSCRICAO_WITH_USER).where(Inscricao.id == inscricao_id)
    inscricao = db.scalars(stmt).first()
    if not inscricao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")
    return inscricao


def update_status(db: Session, inscricao_id: UUID, novo_status: InscricaoStatus) -> Inscricao:
    inscricao = _get_inscricao_or_404(db, inscricao_id)
    if inscricao.status == novo_status:
        return inscricao

    allowed = ALLOWED_TRANSITIONS.get(inscricao.status, set())
    if novo_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transição de status não permitida",
        )

    percentual = float(inscricao.percentual_presenca or 0)
    if novo_status == InscricaoStatus.CONCLUIDO and percentual < 75:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Presença mínima de 75% não atingida",
        )

    inscricao.status = novo_status
    if novo_status == InscricaoStatus.CONCLUIDO:
        if not inscricao.data_conclusao:
            inscricao.data_conclusao = datetime.now(timezone.utc)
        inscricao.apto_certificado = True
    else:
        inscricao.apto_certificado = False
        if novo_status in {InscricaoStatus.ABANDONOU, InscricaoStatus.CANCELADO}:
            inscricao.data_conclusao = None

    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)
    return inscricao
