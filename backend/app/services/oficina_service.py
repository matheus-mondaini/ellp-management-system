"""Business logic for Oficina management (RF-003/RF-004)."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Oficina, Professor, Tema
from ..models.oficina import OficinaStatus
from ..schemas import OficinaCreate, OficinaUpdate


def _get_professor_or_404(db: Session, professor_id: UUID) -> Professor:
    professor = db.get(Professor, professor_id)
    if not professor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
    return professor


def _resolve_temas(db: Session, tema_ids: list[UUID]) -> list[Tema]:
    if not tema_ids:
        return []
    stmt = select(Tema).where(Tema.id.in_(tema_ids))
    temas = db.scalars(stmt).all()
    found_ids = {tema.id for tema in temas}
    missing = set(tema_ids) - found_ids
    if missing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tema não encontrado")
    return temas


def list_oficinas(
    db: Session,
    *,
    status_filter: OficinaStatus | None = None,
    tema_id: UUID | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Oficina]:
    stmt = select(Oficina).order_by(Oficina.data_inicio.asc(), Oficina.titulo.asc())
    if status_filter:
        stmt = stmt.where(Oficina.status == status_filter)
    if start_date:
        stmt = stmt.where(Oficina.data_inicio >= start_date)
    if end_date:
        stmt = stmt.where(Oficina.data_fim <= end_date)
    if tema_id:
        stmt = stmt.join(Oficina.temas).where(Tema.id == tema_id).distinct()
    return db.scalars(stmt).all()


def get_oficina(db: Session, oficina_id: UUID) -> Oficina:
    oficina = db.get(Oficina, oficina_id)
    if not oficina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oficina não encontrada")
    return oficina


def create_oficina(db: Session, payload: OficinaCreate) -> Oficina:
    _get_professor_or_404(db, payload.professor_id)
    temas = _resolve_temas(db, payload.tema_ids)

    oficina = Oficina(
        professor_id=payload.professor_id,
        titulo=payload.titulo,
        descricao=payload.descricao,
        carga_horaria=payload.carga_horaria,
        capacidade_maxima=payload.capacidade_maxima,
        data_inicio=payload.data_inicio,
        data_fim=payload.data_fim,
        local=payload.local,
        status=payload.status,
        temas=temas,
    )
    db.add(oficina)
    db.commit()
    db.refresh(oficina)
    return oficina


def update_oficina(db: Session, oficina_id: UUID, payload: OficinaUpdate) -> Oficina:
    oficina = get_oficina(db, oficina_id)
    data = payload.model_dump(exclude_unset=True)

    tema_ids = data.pop("tema_ids", None)
    if tema_ids is not None:
        oficina.temas = _resolve_temas(db, tema_ids)

    professor_id = data.pop("professor_id", None)
    if professor_id is not None:
        _get_professor_or_404(db, professor_id)
        oficina.professor_id = professor_id

    for field, value in data.items():
        setattr(oficina, field, value)

    db.add(oficina)
    db.commit()
    db.refresh(oficina)
    return oficina


def delete_oficina(db: Session, oficina_id: UUID) -> None:
    oficina = get_oficina(db, oficina_id)
    db.delete(oficina)
    db.commit()
