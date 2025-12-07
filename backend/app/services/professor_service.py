"""Business logic for professor listings (RF-012)."""
from __future__ import annotations

from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Oficina, Professor, Pessoa


def list_professores(db: Session) -> Sequence[Professor]:
    stmt = (
        select(Professor)
        .options(selectinload(Professor.pessoa).selectinload(Pessoa.user))
        .order_by(Professor.created_at.desc())
    )
    return db.scalars(stmt).all()


def get_professor(db: Session, professor_id: UUID) -> Professor:
    stmt = (
        select(Professor)
        .options(
            selectinload(Professor.pessoa).selectinload(Pessoa.user),
            selectinload(Professor.oficinas),
        )
        .where(Professor.id == professor_id)
    )
    professor = db.scalars(stmt).first()
    if not professor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
    return professor