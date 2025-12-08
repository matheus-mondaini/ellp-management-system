"""API tests for RF-014/RF-015 (Relatórios)."""
from datetime import timedelta

from fastapi import status

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


def _registrar_presencas(
    client,
    headers,
    oficina_id,
    registros,
    data_aula,
):
    response = client.post(
        f"/presencas/oficinas/{oficina_id}",
        headers=headers,
        json={"data_aula": str(data_aula), "registros": registros},
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_relatorio_frequencia_agrega_metricas(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
    second_aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    insc1 = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)
    insc2 = _criar_inscricao(client, admin_headers, oficina.id, second_aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    _registrar_presencas(
        client,
        tutor_headers,
        oficina.id,
        [
            {"inscricao_id": insc1, "presente": True},
            {"inscricao_id": insc2, "presente": False},
        ],
        oficina.data_inicio,
    )

    response = client.get(
        f"/relatorios/frequencia/{oficina.id}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["resumo"]["total_inscricoes"] == 2
    assert len(data["alunos"]) == 2
    percentuais = {item["inscricao_id"]: item["percentual_presenca"] for item in data["alunos"]}
    assert percentuais[insc1] == 100.0
    assert percentuais[insc2] == 0.0


def test_relatorio_certificados_resumo_e_pendentes(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
    second_aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    insc_pending = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)
    insc_emitido = _criar_inscricao(client, admin_headers, oficina.id, second_aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    client.patch(
        f"/inscricoes/{insc_pending}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )
    client.patch(
        f"/inscricoes/{insc_emitido}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )

    _registrar_presencas(
        client,
        tutor_headers,
        oficina.id,
        [{"inscricao_id": insc_pending, "presente": True}],
        oficina.data_inicio,
    )
    _registrar_presencas(
        client,
        tutor_headers,
        oficina.id,
        [{"inscricao_id": insc_emitido, "presente": True}],
        oficina.data_inicio + timedelta(days=1),
    )

    client.post(
        f"/certificados/inscricoes/{insc_emitido}",
        headers=tutor_headers,
    )

    response = client.get("/relatorios/certificados", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["resumo"]["total_emitidos"] == 1
    assert payload["resumo"]["pendentes_para_emitir"] == 1
    assert len(payload["certificados"]) == 1
    assert len(payload["pendentes"]) == 1
    assert payload["pendentes"][0]["id"] in {insc_pending, insc_emitido}


def test_relatorio_certificados_restrito_para_admin(
    client,
    tutor_user,
):
    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.get("/relatorios/certificados", headers=tutor_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN