"""Unit tests covering Tema and Oficina ORM modeling."""
from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Oficina, Tema
from app.models.oficina import OficinaStatus


def test_tema_name_is_unique(db_session):
    nome = "Robotica Kids"
    db_session.add(Tema(nome=nome))
    db_session.commit()

    db_session.add(Tema(nome=nome))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_oficina_relates_professor_and_temas(db_session, professor_entity, tema):
    oficina = Oficina(
        professor_id=professor_entity.id,
        titulo="Robotica Criativa",
        descricao="Oficina pratica focada em logica e robotica educacional",
        carga_horaria=12,
        capacidade_maxima=15,
        data_inicio=date(2025, 1, 10),
        data_fim=date(2025, 2, 1),
        local="UTFPR - Bloco E",
        status=OficinaStatus.INSCRICOES_ABERTAS,
        temas=[tema],
    )
    db_session.add(oficina)
    db_session.commit()
    db_session.refresh(oficina)

    assert oficina.professor.id == professor_entity.id
    assert tema in oficina.temas
    assert oficina in professor_entity.oficinas