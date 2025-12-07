"""Pytest fixtures for backend tests."""
from __future__ import annotations

import uuid
from collections.abc import Iterator
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models import Base, Oficina, Pessoa, Professor, Tema, User
from app.models.oficina import OficinaStatus
from app.utils import get_password_hash

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture(autouse=True)
def prepare_database() -> Iterator[None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Iterator[Session]:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def override_get_db() -> Iterator[None]:
    def _get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def _seed_user(
    session: Session,
    *,
    email: str,
    password: str,
    role: str,
    nome: str,
    telefone: str | None = None,
) -> User:
    user = User(email=email, senha_hash=get_password_hash(password), role=role, ativo=True)
    Pessoa(user=user, nome_completo=nome, telefone=telefone, data_nascimento=date(1990, 1, 1))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture()
def admin_user(db_session: Session) -> User:
    return _seed_user(
        db_session,
        email="admin@ellp.test",
        password="admin12345",
        role="admin",
        nome="Administrador",
    )


@pytest.fixture()
def professor_user(db_session: Session) -> User:
    return _seed_user(
        db_session,
        email="prof@ellp.test",
        password="prof12345",
        role="professor",
        nome="Professor",
    )


@pytest.fixture()
def tutor_user(db_session: Session) -> User:
    return _seed_user(
        db_session,
        email="tutor@ellp.test",
        password="tutor12345",
        role="tutor",
        nome="Tutor",
    )


@pytest.fixture()
def aluno_user(db_session: Session) -> User:
    return _seed_user(
        db_session,
        email="aluno@ellp.test",
        password="aluno12345",
        role="aluno",
        nome="Aluno",
    )


@pytest.fixture()
def professor_entity(db_session: Session, professor_user: User) -> Professor:
    professor = Professor(
        pessoa=professor_user.pessoa,
        faculdade="UTFPR",
        departamento="Computacao",
        titulacao="Mestre",
        email_institucional="professor@ellp.test",
        segundo_email=None,
        coordenador=False,
        area_atuacao="Robotica",
        observacoes=None,
    )
    db_session.add(professor)
    db_session.commit()
    db_session.refresh(professor)
    return professor


@pytest.fixture()
def tema(db_session: Session) -> Tema:
    tema = Tema(nome=f"Tema {uuid.uuid4().hex[:8]}", descricao="Robotica e programacao")
    db_session.add(tema)
    db_session.commit()
    db_session.refresh(tema)
    return tema


@pytest.fixture()
def oficina(db_session: Session, professor_entity: Professor, tema: Tema) -> Oficina:
    oficina = Oficina(
        professor_id=professor_entity.id,
        titulo="Robotica Criativa",
        descricao="Oficina pratica",
        carga_horaria=10,
        capacidade_maxima=20,
        data_inicio=date(2025, 1, 10),
        data_fim=date(2025, 1, 20),
        local="UTFPR",
        status=OficinaStatus.PLANEJADA,
        temas=[tema],
    )
    db_session.add(oficina)
    db_session.commit()
    db_session.refresh(oficina)
    return oficina
