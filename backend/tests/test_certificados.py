"""API tests for RF-008/RF-033/RF-034/RF-035 (Certificados)."""

from fastapi import status

from app.models.oficina import OficinaStatus


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


def _registrar_presenca_completa(client, headers, oficina_id, inscricao_id, data_aula):
    response = client.post(
        f"/presencas/oficinas/{oficina_id}",
        headers=headers,
        json={
            "data_aula": str(data_aula),
            "registros": [
                {
                    "inscricao_id": inscricao_id,
                    "presente": True,
                }
            ],
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def _preparar_certificado_tutor(db_session, oficina, tutor_entity):
    oficina.status = OficinaStatus.CONCLUIDA
    oficina.tutores.append(tutor_entity)
    db_session.add(oficina)
    db_session.commit()


def test_emite_certificado_para_inscricao_concluida(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )
    _registrar_presenca_completa(
        client,
        tutor_headers,
        oficina.id,
        inscricao_id,
        oficina.data_inicio,
    )

    response = client.post(
        f"/certificados/inscricoes/{inscricao_id}",
        headers=tutor_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert payload["inscricao_id"] == inscricao_id
    assert payload["tipo"] == "conclusao_aluno"

    listing = client.get("/certificados", headers=admin_headers)
    assert listing.status_code == status.HTTP_200_OK
    assert len(listing.json()) == 1


def test_nao_emite_certificado_sem_conclusao(
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
        f"/certificados/inscricoes/{inscricao_id}",
        headers=tutor_headers,
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_download_certificado_retorna_url(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )
    _registrar_presenca_completa(
        client,
        tutor_headers,
        oficina.id,
        inscricao_id,
        oficina.data_inicio,
    )

    emissao = client.post(
        f"/certificados/inscricoes/{inscricao_id}",
        headers=tutor_headers,
    )
    certificado_id = emissao.json()["id"]

    download = client.get(
        f"/certificados/{certificado_id}/download",
        headers=admin_headers,
    )

    assert download.status_code == status.HTTP_200_OK
    body = download.json()
    assert body["arquivo_pdf_url"].startswith("https://")
    assert body["hash_validacao"]
    assert body["codigo_verificacao"]


def test_aluno_nao_lista_certificados(
    client,
    admin_user,
    tutor_user,
    aluno_user,
    oficina,
    aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )
    _registrar_presenca_completa(
        client,
        tutor_headers,
        oficina.id,
        inscricao_id,
        oficina.data_inicio,
    )
    client.post(f"/certificados/inscricoes/{inscricao_id}", headers=tutor_headers)

    aluno_headers = _auth_headers(client, aluno_user.email, "aluno12345")
    resposta = client.get("/certificados", headers=aluno_headers)

    assert resposta.status_code == status.HTTP_403_FORBIDDEN


def test_admin_emite_certificado_para_tutor(
    client,
    admin_user,
    tutor_entity,
    oficina,
    db_session,
):
    _preparar_certificado_tutor(db_session, oficina, tutor_entity)

    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.post(
        f"/certificados/oficinas/{oficina.id}/tutores/{tutor_entity.id}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert payload["tutor_id"] == str(tutor_entity.id)
    assert payload["tipo"] == "participacao_tutor"

    duplicate = client.post(
        f"/certificados/oficinas/{oficina.id}/tutores/{tutor_entity.id}",
        headers=admin_headers,
    )
    assert duplicate.status_code == status.HTTP_409_CONFLICT


def test_tutor_lista_e_baixa_certificado_proprio(
    client,
    admin_user,
    tutor_user,
    tutor_entity,
    oficina,
    db_session,
):
    _preparar_certificado_tutor(db_session, oficina, tutor_entity)
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    emissao = client.post(
        f"/certificados/oficinas/{oficina.id}/tutores/{tutor_entity.id}",
        headers=admin_headers,
    ).json()

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    lista = client.get("/certificados/tutores/me", headers=tutor_headers)
    assert lista.status_code == status.HTTP_200_OK
    itens = lista.json()
    assert len(itens) == 1
    assert itens[0]["id"] == emissao["id"]

    download = client.get(
        f"/certificados/{emissao['id']}/download",
        headers=tutor_headers,
    )
    assert download.status_code == status.HTTP_200_OK


def test_tutor_nao_baixa_certificado_de_aluno(
    client,
    admin_user,
    tutor_user,
    tutor_entity,
    oficina,
    aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )
    _registrar_presenca_completa(
        client,
        tutor_headers,
        oficina.id,
        inscricao_id,
        oficina.data_inicio,
    )
    emissao = client.post(
        f"/certificados/inscricoes/{inscricao_id}",
        headers=tutor_headers,
    )

    certificado_id = emissao.json()["id"]
    resposta = client.get(
        f"/certificados/{certificado_id}/download",
        headers=tutor_headers,
    )

    assert resposta.status_code == status.HTTP_403_FORBIDDEN


def test_validacao_publica_retorna_dados(
    client,
    admin_user,
    tutor_user,
    oficina,
    aluno_entity,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    client.patch(
        f"/inscricoes/{inscricao_id}/status",
        headers=tutor_headers,
        json={"status": "em_andamento"},
    )
    _registrar_presenca_completa(
        client,
        tutor_headers,
        oficina.id,
        inscricao_id,
        oficina.data_inicio,
    )
    emissao = client.post(
        f"/certificados/inscricoes/{inscricao_id}",
        headers=tutor_headers,
    )

    hash_validacao = emissao.json()["hash_validacao"]
    resposta = client.get(f"/certificados/validar/{hash_validacao}")

    assert resposta.status_code == status.HTTP_200_OK
    body = resposta.json()
    assert body["hash_validacao"] == hash_validacao
    assert body["participante_nome"] == aluno_entity.pessoa.nome_completo
    assert body["valido"] is True


def test_validacao_publica_hash_invalido(client):
    resposta = client.get("/certificados/validar/hash-invalido")
    assert resposta.status_code == status.HTTP_404_NOT_FOUND
