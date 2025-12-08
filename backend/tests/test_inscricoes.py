"""API tests for RF-005 (Inscrição de Alunos)."""
from datetime import date, timedelta

from fastapi import status

from app.models.oficina import OficinaStatus


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_inscreve_aluno_com_sucesso(client, admin_user, oficina, aluno_entity):
    headers = _auth_headers(client, admin_user.email, "admin12345")

    response = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_entity.id)},
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert payload["aluno_id"] == str(aluno_entity.id)
    assert payload["status"] == "inscrito"


def test_nao_permite_inscricao_duplicada(client, admin_user, oficina, aluno_entity):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_entity.id)},
    )

    response = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_entity.id)},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_respeita_capacidade_maxima(
    client,
    admin_user,
    oficina,
    aluno_entity,
    second_aluno_entity,
    db_session,
):
    oficina.capacidade_maxima = 1
    db_session.add(oficina)
    db_session.commit()

    headers = _auth_headers(client, admin_user.email, "admin12345")
    client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_entity.id)},
    )

    response = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(second_aluno_entity.id)},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_oficina_encerrada_rejeita_inscricao(client, admin_user, oficina, aluno_entity, db_session):
    oficina.status = OficinaStatus.CONCLUIDA
    oficina.data_inicio = date.today() - timedelta(days=20)
    oficina.data_fim = date.today() - timedelta(days=1)
    db_session.add(oficina)
    db_session.commit()

    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_entity.id)},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_aluno_nao_pode_criar_inscricao(client, aluno_user, aluno_entity, oficina):
    headers = _auth_headers(client, aluno_user.email, "aluno12345")

    response = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_entity.id)},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_listagem_de_inscricoes(client, admin_user, oficina, aluno_entity):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json={"aluno_id": str(aluno_entity.id)},
    )

    response = client.get(f"/oficinas/{oficina.id}/inscricoes", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["aluno_nome"] == aluno_entity.pessoa.nome_completo


def test_tutor_atualiza_status_para_em_andamento(client, admin_user, tutor_user, oficina, aluno_entity):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=admin_headers,
        json={"aluno_id": str(aluno_entity.id)},
    ).json()["id"]

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["status"] == "em_andamento"
    assert payload["percentual_presenca"] == 0


def test_nao_conclui_sem_presenca_minima(client, admin_user, tutor_user, oficina, aluno_entity):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=admin_headers,
        json={"aluno_id": str(aluno_entity.id)},
    ).json()["id"]

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "concluido"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_conclusao_automatica_depois_de_presencas(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=admin_headers,
        json={"aluno_id": str(aluno_entity.id)},
    ).json()["id"]

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )

    client.post(
        f"/presencas/oficinas/{oficina.id}",
        headers=tutor_headers,
        json={
            "data_aula": str(oficina.data_inicio),
            "registros": [{"inscricao_id": inscricao_id, "presente": True}],
        },
    )

    response = client.get(f"/oficinas/{oficina.id}/inscricoes", headers=admin_headers)
    dados = response.json()[0]
    assert dados["status"] == "concluido"
    assert dados["apto_certificado"] is True
    assert dados["percentual_presenca"] == 100.0


def test_aluno_nao_atualiza_status(client, admin_user, aluno_user, oficina, aluno_entity):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=admin_headers,
        json={"aluno_id": str(aluno_entity.id)},
    ).json()["id"]

    aluno_headers = _auth_headers(client, aluno_user.email, "aluno12345")
    response = client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=aluno_headers,
        json={"status": "em_andamento"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
