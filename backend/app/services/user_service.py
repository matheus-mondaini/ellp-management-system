"""Business rules for creating and listing users."""
from __future__ import annotations

from datetime import date
from typing import Iterable

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Aluno, Pessoa, Professor, Tutor, User
from ..schemas import AlunoCreate, ProfessorCreate, TutorCreate, UserRead
from ..utils import get_password_hash


ROLE_MAP = {
    "aluno": "aluno",
    "tutor": "tutor",
    "professor": "professor",
}


def _ensure_email_available(db: Session, email: str) -> None:
    exists = db.execute(select(User.id).where(User.email == email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já utilizado")


def _build_user_core(
    role: str,
    *,
    email: str,
    password: str,
    nome_completo: str,
    telefone: str | None,
    data_nascimento: date | None,
) -> tuple[User, Pessoa]:
    user = User(email=email, senha_hash=get_password_hash(password), role=role)
    pessoa = Pessoa(
        user=user,
        nome_completo=nome_completo,
        telefone=telefone,
        data_nascimento=data_nascimento,
    )
    return user, pessoa


def create_aluno(db: Session, payload: AlunoCreate) -> User:
    _ensure_email_available(db, payload.email)
    user, pessoa = _build_user_core(
        ROLE_MAP["aluno"],
        email=payload.email,
        password=payload.password,
        nome_completo=payload.nome_completo,
        telefone=payload.telefone,
        data_nascimento=payload.data_nascimento,
    )
    Aluno(
        pessoa=pessoa,
        escola=payload.escola,
        serie=payload.serie,
        responsavel_nome=payload.responsavel_nome,
        responsavel_telefone=payload.responsavel_telefone,
        responsavel_email=payload.responsavel_email,
        endereco_cidade=payload.endereco_cidade,
        endereco_uf=payload.endereco_uf,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_tutor(db: Session, payload: TutorCreate) -> User:
    _ensure_email_available(db, payload.email)
    user, pessoa = _build_user_core(
        ROLE_MAP["tutor"],
        email=payload.email,
        password=payload.password,
        nome_completo=payload.nome_completo,
        telefone=payload.telefone,
        data_nascimento=payload.data_nascimento,
    )
    Tutor(
        pessoa=pessoa,
        faculdade=payload.faculdade,
        curso=payload.curso,
        semestre=payload.semestre,
        email_educacional=payload.email_educacional,
        tipo_vinculo=payload.tipo_vinculo,
        carga_horaria_maxima_semanal=payload.carga_horaria_maxima_semanal,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_professor(db: Session, payload: ProfessorCreate) -> User:
    _ensure_email_available(db, payload.email)
    user, pessoa = _build_user_core(
        ROLE_MAP["professor"],
        email=payload.email,
        password=payload.password,
        nome_completo=payload.nome_completo,
        telefone=payload.telefone,
        data_nascimento=payload.data_nascimento,
    )
    Professor(
        pessoa=pessoa,
        faculdade=payload.faculdade,
        departamento=payload.departamento,
        titulacao=payload.titulacao,
        email_institucional=payload.email_institucional,
        coordenador=payload.coordenador,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users_by_role(db: Session, role: str) -> Iterable[User]:
    stmt = select(User).where(User.role == role).order_by(User.created_at.desc())
    return db.scalars(stmt).all()


def to_user_read(user: User) -> UserRead:
    nome = user.pessoa.nome_completo if user.pessoa else ""
    return UserRead(
        id=user.id,
        email=user.email,
        role=user.role,
        nome_completo=nome,
        ativo=user.ativo,
    )
