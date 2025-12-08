"""API tests for RF-007 (Registro de Presenças)."""
from datetime import timedelta
from uuid import UUID

from fastapi import status

from app.models import Inscricao


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _criar_inscricao(client, headers, oficina_id, aluno_id) -> str:
    response = client.post(
        f"/oficinas/{oficina_id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_id)},
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


def test_tutor_registra_presencas_atualiza_percentual(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
    second_aluno_entity,
    db_session,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    insc1 = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)
    insc2 = _criar_inscricao(client, admin_headers, oficina.id, second_aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    data_aula = str(oficina.data_inicio)
    response = client.post(
        f"/presencas/oficinas/{oficina.id}",
        headers=tutor_headers,
        json={
            "data_aula": data_aula,
            "registros": [
                {"inscricao_id": insc1, "presente": True},
                {"inscricao_id": insc2, "presente": False, "justificativa": "Doente"},
            ],
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert len(payload) == 2
    assert {item["inscricao_id"] for item in payload} == {insc1, insc2}

    primeira = db_session.get(Inscricao, UUID(insc1))
    segunda = db_session.get(Inscricao, UUID(insc2))
    assert float(primeira.percentual_presenca) == 100.0
    assert primeira.total_presencas == 1
    assert float(segunda.percentual_presenca) == 0.0
    assert segunda.total_faltas == 1


def test_rejeita_registro_fora_do_periodo_da_oficina(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.post(
        f"/presencas/oficinas/{oficina.id}",
        headers=tutor_headers,
        json={
            "data_aula": str(oficina.data_inicio - timedelta(days=5)),
            "registros": [{"inscricao_id": inscricao_id, "presente": True}],
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_aluno_nao_pode_registrar_presenca(client, admin_user, aluno_user, oficina, aluno_entity):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    aluno_headers = _auth_headers(client, aluno_user.email, "aluno12345")
    response = client.post(
        f"/presencas/oficinas/{oficina.id}",
        headers=aluno_headers,
        json={
            "data_aula": str(oficina.data_inicio),
            "registros": [{"inscricao_id": inscricao_id, "presente": True}],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_listagem_filtra_por_data(client, admin_user, tutor_user, oficina, aluno_entity):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    primeira_data = str(oficina.data_inicio)
    segunda_data = str(oficina.data_inicio + timedelta(days=1))

    client.post(
        f"/presencas/oficinas/{oficina.id}",
        headers=tutor_headers,
        json={
            "data_aula": primeira_data,
            "registros": [{"inscricao_id": inscricao_id, "presente": True}],
        },
    )
    client.post(
        f"/presencas/oficinas/{oficina.id}",
        headers=tutor_headers,
        json={
            "data_aula": segunda_data,
            "registros": [{"inscricao_id": inscricao_id, "presente": False}],
        },
    )

    filtrado = client.get(
        f"/presencas/oficinas/{oficina.id}",
        headers=tutor_headers,
        params={"data_aula": segunda_data},
    )

    assert filtrado.status_code == status.HTTP_200_OK
    data = filtrado.json()
    assert len(data) == 1
    assert data[0]["data_aula"] == segunda_data
    assert data[0]["presente"] is False


def test_patch_e_delete_presenca_atualizam_metricas(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
    db_session,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    resposta = client.post(
        f"/presencas/oficinas/{oficina.id}",
        headers=tutor_headers,
        json={
            "data_aula": str(oficina.data_inicio),
            "registros": [{"inscricao_id": inscricao_id, "presente": True}],
        },
    )
    presenca_id = resposta.json()[0]["id"]

    patch = client.patch(
        f"/presencas/{presenca_id}",
        headers=tutor_headers,
        json={"presente": False, "justificativa": "Febre"},
    )

    assert patch.status_code == status.HTTP_200_OK
    assert patch.json()["presente"] is False

    inscricao = db_session.get(Inscricao, UUID(inscricao_id))
    assert float(inscricao.percentual_presenca) == 0.0
    assert inscricao.total_presencas == 0

    delete = client.delete(f"/presencas/{presenca_id}", headers=tutor_headers)
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    db_session.refresh(inscricao)
    assert float(inscricao.percentual_presenca) == 0.0
    assert inscricao.total_presencas == 0
    assert inscricao.total_faltas == 0
