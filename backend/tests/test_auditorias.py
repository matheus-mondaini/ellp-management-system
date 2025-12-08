"""API tests for RF-021 (Auditoria de Ações)."""
from datetime import date, timedelta

from fastapi import status


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _nova_oficina_payload(professor_id, tema_id):
    inicio = date.today() + timedelta(days=5)
    fim = inicio + timedelta(days=2)
    return {
        "titulo": "Oficina Auditoria",
        "descricao": "Testando logs",
        "carga_horaria": 8,
        "capacidade_maxima": 15,
        "data_inicio": str(inicio),
        "data_fim": str(fim),
        "local": "UTFPR",
        "status": "planejada",
        "professor_id": str(professor_id),
        "tema_ids": [str(tema_id)],
    }


def test_auditoria_registra_criacao_de_oficina(client, admin_user, professor_entity, tema):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    payload = _nova_oficina_payload(professor_entity.id, tema.id)

    response = client.post("/oficinas", json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    audit_response = client.get("/auditorias", headers=headers)
    assert audit_response.status_code == status.HTTP_200_OK
    itens = audit_response.json()
    assert len(itens) >= 1
    evento = itens[0]
    assert evento["entidade"] == "oficina"
    assert evento["acao"] == "criada"
    assert evento["user_email"] == admin_user.email


def test_listagem_de_auditoria_restrita_a_admin(client, tutor_user):
    tutor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.get("/auditorias", headers=tutor_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
