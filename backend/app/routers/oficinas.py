"""Endpoints for managing oficinas (RF-003/RF-004)."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models.oficina import OficinaStatus
from ..schemas import OficinaCreate, OficinaRead, OficinaUpdate
from ..services import oficina_service

router = APIRouter(prefix="/oficinas", tags=["oficinas"])

AdminOrProfessor = Depends(require_role(["admin", "professor"]))
TutorOrHigher = Depends(require_role(["admin", "professor", "tutor"]))


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
    _: None = AdminOrProfessor,
) -> OficinaRead:
    return oficina_service.create_oficina(db, payload)


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
    _: None = AdminOrProfessor,
) -> OficinaRead:
    return oficina_service.update_oficina(db, oficina_id, payload)


@router.delete("/{oficina_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_oficina(
    oficina_id: UUID,
    db: Session = Depends(get_db),
    _: None = AdminOrProfessor,
) -> Response:
    oficina_service.delete_oficina(db, oficina_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
