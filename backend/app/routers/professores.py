"""Endpoints for professor management (RF-012)."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import UserRole
from ..schemas import ProfessorDetailRead, ProfessorRead
from ..services import professor_service

router = APIRouter(prefix="/professores", tags=["professores"])

TutorOrHigher = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR, UserRole.TUTOR]))


@router.get("", response_model=list[ProfessorRead])
def list_professores(
    db: Session = Depends(get_db),
    _: None = TutorOrHigher,
) -> list[ProfessorRead]:
    professores = professor_service.list_professores(db)
    return [
        ProfessorRead(
            id=prof.id,
            nome=prof.pessoa.nome_completo,
            email=prof.pessoa.user.email,
            faculdade=prof.faculdade,
            departamento=prof.departamento,
            coordenador=prof.coordenador,
        )
        for prof in professores
    ]


@router.get("/{professor_id}", response_model=ProfessorDetailRead)
def retrieve_professor(
    professor_id: UUID,
    db: Session = Depends(get_db),
    _: None = TutorOrHigher,
) -> ProfessorDetailRead:
    professor = professor_service.get_professor(db, professor_id)
    return ProfessorDetailRead(
        id=professor.id,
        nome=professor.pessoa.nome_completo,
        email=professor.pessoa.user.email,
        faculdade=professor.faculdade,
        departamento=professor.departamento,
        coordenador=professor.coordenador,
        area_atuacao=professor.area_atuacao,
        observacoes=professor.observacoes,
        oficinas=professor.oficinas,
    )