"""Regras de negócio para RF-007 (Registro de Presenças)."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from ..models import Aluno, Inscricao, Oficina, Pessoa, Presenca
from ..models.inscricao import InscricaoStatus
from ..schemas.presenca import PresencaRegistro, PresencaUpdate

PRESENCA_RELATIONS = (
    selectinload(Presenca.inscricao)
    .selectinload(Inscricao.aluno)
    .selectinload(Aluno.pessoa)
    .selectinload(Pessoa.user)
)


def _with_relations(stmt):
    return stmt.options(
        PRESENCA_RELATIONS,
        selectinload(Presenca.registrado_por_user),
    )


def _get_oficina_or_404(db: Session, oficina_id: UUID) -> Oficina:
    oficina = db.get(Oficina, oficina_id)
    if not oficina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oficina não encontrada")
    return oficina


def _ensure_date_within_range(oficina: Oficina, data_aula: date) -> None:
    if data_aula < oficina.data_inicio or data_aula > oficina.data_fim:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Data da presença fora do período da oficina",
        )


def _load_inscricoes_or_raise(db: Session, oficina_id: UUID, inscricao_ids: set[UUID]) -> dict[UUID, Inscricao]:
    if not inscricao_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum registro informado")

    stmt = select(Inscricao).where(
        Inscricao.oficina_id == oficina_id,
        Inscricao.id.in_(inscricao_ids),
    )
    items = {inscricao.id: inscricao for inscricao in db.scalars(stmt)}
    missing = inscricao_ids - set(items.keys())
    if missing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")
    return items


def _recalculate_inscricao_stats(db: Session, inscricao_id: UUID) -> None:
    total_registros = db.scalar(
        select(func.count(Presenca.id)).where(Presenca.inscricao_id == inscricao_id)
    )
    total_registros = total_registros or 0
    total_presentes = db.scalar(
        select(func.count(Presenca.id)).where(
            Presenca.inscricao_id == inscricao_id,
            Presenca.presente.is_(True),
        )
    )
    total_presentes = total_presentes or 0
    total_faltas = max(total_registros - total_presentes, 0)
    percentual = round((total_presentes / total_registros) * 100, 2) if total_registros else 0.0

    inscricao = db.get(Inscricao, inscricao_id)
    if not inscricao:
        return

    inscricao.total_presencas = total_presentes
    inscricao.total_faltas = total_faltas
    inscricao.total_aulas_previstas = max(total_registros, inscricao.total_aulas_previstas or 0)
    inscricao.percentual_presenca = percentual
    inscricao.apto_certificado = bool(
        inscricao.status == InscricaoStatus.CONCLUIDO and percentual >= 75.0
    )
    db.add(inscricao)


def _fetch_presencas_by_ids(db: Session, presenca_ids: list[UUID]) -> list[Presenca]:
    if not presenca_ids:
        return []
    stmt = select(Presenca).where(Presenca.id.in_(presenca_ids)).order_by(
        Presenca.data_aula.asc(), Presenca.created_at.asc()
    )
    stmt = _with_relations(stmt)
    return db.scalars(stmt).all()


def list_by_oficina(
    db: Session,
    oficina_id: UUID,
    *,
    data_aula: date | None = None,
) -> list[Presenca]:
    _get_oficina_or_404(db, oficina_id)
    stmt = (
        select(Presenca)
        .join(Presenca.inscricao)
        .where(Inscricao.oficina_id == oficina_id)
        .order_by(Presenca.data_aula.asc(), Presenca.created_at.asc())
    )
    if data_aula:
        stmt = stmt.where(Presenca.data_aula == data_aula)
    stmt = _with_relations(stmt)
    return db.scalars(stmt).all()


def list_by_inscricao(db: Session, inscricao_id: UUID) -> list[Presenca]:
    inscricao = db.get(Inscricao, inscricao_id)
    if not inscricao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")
    stmt = (
        select(Presenca)
        .where(Presenca.inscricao_id == inscricao_id)
        .order_by(Presenca.data_aula.asc(), Presenca.created_at.asc())
    )
    stmt = _with_relations(stmt)
    return db.scalars(stmt).all()


def registrar_lote(
    db: Session,
    oficina_id: UUID,
    *,
    data_aula: date,
    registros: list[PresencaRegistro],
    registrador_id: UUID,
) -> list[Presenca]:
    if not registros:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum registro informado")

    oficina = _get_oficina_or_404(db, oficina_id)
    _ensure_date_within_range(oficina, data_aula)

    inscricao_ids = [item.inscricao_id for item in registros]
    duplicates = len(inscricao_ids) != len(set(inscricao_ids))
    if duplicates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inscrições duplicadas no payload",
        )

    inscricoes = _load_inscricoes_or_raise(db, oficina_id, set(inscricao_ids))
    for inscricao in inscricoes.values():
        if inscricao.status in (InscricaoStatus.CANCELADO, InscricaoStatus.ABANDONOU):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Inscrição não permite registro de presença",
            )

    touched: set[UUID] = set()
    persisted: list[Presenca] = []

    for registro in registros:
        presenca = db.execute(
            select(Presenca).where(
                Presenca.inscricao_id == registro.inscricao_id,
                Presenca.data_aula == data_aula,
            )
        ).scalar_one_or_none()

        if presenca is None:
            presenca = Presenca(
                inscricao_id=registro.inscricao_id,
                data_aula=data_aula,
            )

        presenca.numero_aula = registro.numero_aula
        presenca.presente = registro.presente
        presenca.justificativa = registro.justificativa
        presenca.observacao_tutor = registro.observacao_tutor
        presenca.registrado_por_id = registrador_id
        db.add(presenca)
        persisted.append(presenca)
        touched.add(registro.inscricao_id)

    db.flush()

    for inscricao_id in touched:
        _recalculate_inscricao_stats(db, inscricao_id)

    db.commit()
    return _fetch_presencas_by_ids(db, [item.id for item in persisted])


def update_presenca(
    db: Session,
    presenca_id: UUID,
    payload: PresencaUpdate,
    *,
    registrador_id: UUID,
) -> Presenca:
    presenca = db.get(Presenca, presenca_id)
    if not presenca:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presença não encontrada")

    data = payload.model_dump(exclude_unset=True)
    if not data:
        return _fetch_presencas_by_ids(db, [presenca.id])[0]

    if "data_aula" in data:
        _ensure_date_within_range(presenca.inscricao.oficina, data["data_aula"])
        conflict = db.execute(
            select(Presenca).where(
                Presenca.inscricao_id == presenca.inscricao_id,
                Presenca.data_aula == data["data_aula"],
                Presenca.id != presenca.id,
            )
        ).scalar_one_or_none()
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe presença registrada para esta data",
            )
        presenca.data_aula = data["data_aula"]

    if "numero_aula" in data:
        presenca.numero_aula = data["numero_aula"]
    if "presente" in data:
        presenca.presente = data["presente"]
    if "justificativa" in data:
        presenca.justificativa = data["justificativa"]
    if "observacao_tutor" in data:
        presenca.observacao_tutor = data["observacao_tutor"]

    presenca.registrado_por_id = registrador_id
    db.add(presenca)
    db.flush()
    _recalculate_inscricao_stats(db, presenca.inscricao_id)
    db.commit()

    return _fetch_presencas_by_ids(db, [presenca.id])[0]


def delete_presenca(db: Session, presenca_id: UUID) -> None:
    presenca = db.get(Presenca, presenca_id)
    if not presenca:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presença não encontrada")

    inscricao_id = presenca.inscricao_id
    db.delete(presenca)
    db.flush()
    _recalculate_inscricao_stats(db, inscricao_id)
    db.commit()