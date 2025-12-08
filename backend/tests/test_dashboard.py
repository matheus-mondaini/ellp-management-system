"""API tests for RF-022 (Dashboard)."""
from uuid import uuid4

from fastapi import status

from app.models import Certificado, Inscricao
from app.models.certificado import CertificadoTipo
from app.models.inscricao import InscricaoStatus
from app.models.oficina import OficinaStatus


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_dashboard_metricas_para_admin(
    client,
    db_session,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
    second_aluno_entity,
):
    oficina.status = OficinaStatus.EM_ANDAMENTO
    db_session.commit()

    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    registro1 = Inscricao(
        aluno_id=aluno_entity.id,
        oficina_id=oficina.id,
        status=InscricaoStatus.EM_ANDAMENTO,
        percentual_presenca=100,
    )
    registro2 = Inscricao(
        aluno_id=second_aluno_entity.id,
        oficina_id=oficina.id,
        status=InscricaoStatus.CONCLUIDO,
        percentual_presenca=50,
    )
    db_session.add_all([registro1, registro2])
    db_session.commit()

    certificado = Certificado(
        inscricao_id=registro1.id,
        oficina_id=registro1.oficina_id,
        tipo=CertificadoTipo.CONCLUSAO_ALUNO,
        hash_validacao=f"hash-{uuid4().hex}",
        codigo_verificacao=f"cod-{uuid4().hex[:10]}",
    )
    db_session.add(certificado)
    db_session.commit()

    response = client.get("/dashboard/metricas", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["oficinas_ativas"] == 1
    assert payload["total_inscricoes"] == 2
    assert payload["certificados_emitidos"] == 1
    assert payload["presenca_media_geral"] == 75.0
    assert "ultima_atualizacao" in payload


def test_dashboard_metricas_restrito_para_admin(client, tutor_user):
    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.get("/dashboard/metricas", headers=tutor_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
