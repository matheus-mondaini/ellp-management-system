"""Tema management endpoints."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..schemas import TemaCreate, TemaRead, TemaUpdate
from ..services import tema_service

router = APIRouter(prefix="/temas", tags=["temas"])

AdminAndProfessor = Depends(require_role(["admin", "professor"]))


@router.get("", response_model=list[TemaRead])
def list_temas(
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> list[TemaRead]:
    return tema_service.list_temas(db)


@router.post("", response_model=TemaRead, status_code=status.HTTP_201_CREATED)
def create_tema(
    payload: TemaCreate,
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> TemaRead:
    return tema_service.create_tema(db, payload)


@router.get("/{tema_id}", response_model=TemaRead)
def retrieve_tema(
    tema_id: UUID,
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> TemaRead:
    return tema_service.get_tema(db, tema_id)


@router.patch("/{tema_id}", response_model=TemaRead)
def update_tema(
    tema_id: UUID,
    payload: TemaUpdate,
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> TemaRead:
    return tema_service.update_tema(db, tema_id, payload)


@router.delete("/{tema_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tema(
    tema_id: UUID,
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> Response:
    tema_service.delete_tema(db, tema_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
