"""User CRUD endpoints for admin flows."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import UserRole
from ..schemas import AdminCreate, AlunoCreate, TutorCreate, ProfessorCreate, UserRead
from ..services import user_service

router = APIRouter(prefix="/users", tags=["users"])

AdminOnly = Depends(require_role([UserRole.ADMIN]))
AdminAndProfessor = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR]))


@router.post("/admins", response_model=UserRead, status_code=201)
def create_admin(
    payload: AdminCreate,
    db: Session = Depends(get_db),
    _: None = AdminOnly,
) -> UserRead:
    user = user_service.create_admin(db, payload)
    return user_service.to_user_read(user)


@router.get("/admins", response_model=list[UserRead])
def list_admins(
    db: Session = Depends(get_db),
    _: None = AdminOnly,
) -> list[UserRead]:
    users = user_service.list_users_by_role(db, "admin")
    return [user_service.to_user_read(user) for user in users]


@router.post("/alunos", response_model=UserRead, status_code=201)
def create_aluno(
    payload: AlunoCreate,
    db: Session = Depends(get_db),
    _: None = AdminOnly,
) -> UserRead:
    user = user_service.create_aluno(db, payload)
    return user_service.to_user_read(user)


@router.get("/alunos", response_model=list[UserRead])
def list_alunos(
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> list[UserRead]:
    users = user_service.list_users_by_role(db, "aluno")
    return [user_service.to_user_read(user) for user in users]


@router.post("/tutores", response_model=UserRead, status_code=201)
def create_tutor(
    payload: TutorCreate,
    db: Session = Depends(get_db),
    _: None = AdminOnly,
) -> UserRead:
    user = user_service.create_tutor(db, payload)
    return user_service.to_user_read(user)


@router.get("/tutores", response_model=list[UserRead])
def list_tutores(
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> list[UserRead]:
    users = user_service.list_users_by_role(db, "tutor")
    return [user_service.to_user_read(user) for user in users]


@router.post("/professores", response_model=UserRead, status_code=201)
def create_professor(
    payload: ProfessorCreate,
    db: Session = Depends(get_db),
    _: None = AdminOnly,
) -> UserRead:
    user = user_service.create_professor(db, payload)
    return user_service.to_user_read(user)


@router.get("/professores", response_model=list[UserRead])
def list_professores(
    db: Session = Depends(get_db),
    _: None = AdminAndProfessor,
) -> list[UserRead]:
    users = user_service.list_users_by_role(db, "professor")
    return [user_service.to_user_read(user) for user in users]
