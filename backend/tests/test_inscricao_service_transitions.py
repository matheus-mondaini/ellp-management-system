"""Focused tests for inscricao_service status transitions (RF-031/RF-032)."""
from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.models.inscricao import InscricaoStatus
from app.services import inscricao_service


def test_update_status_progresses_to_em_andamento(db_session, inscricao):
    atualizado = inscricao_service.update_status(
        db_session,
        inscricao.id,
        InscricaoStatus.EM_ANDAMENTO,
    )

    assert atualizado.status == InscricaoStatus.EM_ANDAMENTO
    assert atualizado.apto_certificado is False


def test_update_status_sets_conclusion_metadata(db_session, inscricao):
    inscricao.percentual_presenca = 80
    db_session.add(inscricao)
    db_session.commit()

    inscricao_service.update_status(
        db_session,
        inscricao.id,
        InscricaoStatus.EM_ANDAMENTO,
    )

    concluida = inscricao_service.update_status(
        db_session,
        inscricao.id,
        InscricaoStatus.CONCLUIDO,
    )

    assert concluida.status == InscricaoStatus.CONCLUIDO
    assert concluida.apto_certificado is True
    assert concluida.data_conclusao is not None


def test_update_status_invalid_transition_raises(db_session, inscricao):
    inscricao_service.update_status(db_session, inscricao.id, InscricaoStatus.EM_ANDAMENTO)

    with pytest.raises(HTTPException) as exc:
        inscricao_service.update_status(db_session, inscricao.id, InscricaoStatus.INSCRITO)

    assert exc.value.status_code == 409


def test_update_status_clears_completion_flags_when_cancelled(db_session, inscricao):
    andamento = inscricao_service.update_status(
        db_session,
        inscricao.id,
        InscricaoStatus.EM_ANDAMENTO,
    )
    andamento.data_conclusao = datetime.now(timezone.utc)
    andamento.apto_certificado = True
    db_session.add(andamento)
    db_session.commit()

    cancelada = inscricao_service.update_status(
        db_session,
        andamento.id,
        InscricaoStatus.CANCELADO,
    )

    assert cancelada.status == InscricaoStatus.CANCELADO
    assert cancelada.apto_certificado is False
    assert cancelada.data_conclusao is None
