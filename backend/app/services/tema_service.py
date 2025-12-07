"""Business logic for Tema CRUD operations."""
from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Tema
from ..schemas import TemaCreate, TemaUpdate


def list_temas(db: Session) -> list[Tema]:
    stmt = select(Tema).order_by(Tema.nome.asc())
    return db.scalars(stmt).all()


def get_tema(db: Session, tema_id: UUID) -> Tema:
    tema = db.get(Tema, tema_id)
    if not tema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tema não encontrado")
    return tema


def _ensure_nome_available(db: Session, nome: str, *, exclude_id: UUID | None = None) -> None:
    stmt = select(Tema.id).where(Tema.nome == nome)
    if exclude_id:
        stmt = stmt.where(Tema.id != exclude_id)
    exists = db.execute(stmt).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nome de tema já utilizado")


def create_tema(db: Session, payload: TemaCreate) -> Tema:
    _ensure_nome_available(db, payload.nome)
    tema = Tema(**payload.model_dump())
    db.add(tema)
    db.commit()
    db.refresh(tema)
    return tema


def update_tema(db: Session, tema_id: UUID, payload: TemaUpdate) -> Tema:
    tema = get_tema(db, tema_id)
    data = payload.model_dump(exclude_unset=True)
    if "nome" in data:
        _ensure_nome_available(db, data["nome"], exclude_id=tema.id)
    for field, value in data.items():
        setattr(tema, field, value)
    db.add(tema)
    db.commit()
    db.refresh(tema)
    return tema


def delete_tema(db: Session, tema_id: UUID) -> None:
    tema = get_tema(db, tema_id)
    db.delete(tema)
    db.commit()