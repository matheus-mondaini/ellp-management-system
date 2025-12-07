"""API tests for RF-003 (Cadastro de Oficinas)."""
from datetime import date
from uuid import uuid4

from fastapi import status

from app.models import Tema
from app.models.oficina import OficinaStatus


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_creates_oficina_with_tema(client, admin_user, professor_entity, tema):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    payload = {
        "professor_id": str(professor_entity.id),
        "titulo": "Oficina Robotica",
        "descricao": "Aprendizado com kits Lego",
        "carga_horaria": 12,
        "capacidade_maxima": 18,
        "data_inicio": str(date(2025, 3, 1)),
        "data_fim": str(date(2025, 3, 20)),
        "local": "UTFPR Bloco E",
        "status": OficinaStatus.INSCRICOES_ABERTAS,
        "tema_ids": [str(tema.id)],
    }

    response = client.post("/oficinas", headers=headers, json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["professor_id"] == payload["professor_id"]
    assert data["temas"][0]["id"] == str(tema.id)


def test_create_oficina_with_unknown_professor_returns_404(client, admin_user, tema):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    payload = {
        "professor_id": str(uuid4()),
        "titulo": "Oficina sem professor",
        "carga_horaria": 5,
        "capacidade_maxima": 10,
        "data_inicio": str(date(2025, 5, 10)),
        "data_fim": str(date(2025, 5, 20)),
        "local": "UTFPR",
        "status": OficinaStatus.PLANEJADA,
        "tema_ids": [str(tema.id)],
    }

    response = client.post("/oficinas", headers=headers, json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_professor_updates_oficina_assigns_new_tema(client, professor_user, db_session, oficina):
    headers = _auth_headers(client, professor_user.email, "prof12345")
    novo_tema = Tema(nome="Automacao", descricao="Automacao industrial para jovens")
    db_session.add(novo_tema)
    db_session.commit()
    db_session.refresh(novo_tema)

    response = client.patch(
        f"/oficinas/{oficina.id}",
        headers=headers,
        json={
            "titulo": "Oficina Atualizada",
            "status": OficinaStatus.EM_ANDAMENTO,
            "tema_ids": [str(novo_tema.id)],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["titulo"] == "Oficina Atualizada"
    assert data["status"] == OficinaStatus.EM_ANDAMENTO
    assert [tema["id"] for tema in data["temas"]] == [str(novo_tema.id)]


def test_admin_deletes_oficina(client, admin_user, oficina):
    headers = _auth_headers(client, admin_user.email, "admin12345")

    delete_response = client.delete(f"/oficinas/{oficina.id}", headers=headers)
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    fetch_response = client.get(f"/oficinas/{oficina.id}", headers=headers)
    assert fetch_response.status_code == status.HTTP_404_NOT_FOUND


def test_tutor_cannot_create_oficina(client, tutor_user, professor_entity, tema):
    headers = _auth_headers(client, tutor_user.email, "tutor12345")

    response = client.post(
        "/oficinas",
        headers=headers,
        json={
            "professor_id": str(professor_entity.id),
            "titulo": "Oficina Tutor",
            "carga_horaria": 8,
            "capacidade_maxima": 10,
            "data_inicio": str(date(2025, 4, 1)),
            "data_fim": str(date(2025, 4, 10)),
            "local": "UTFPR",
            "status": OficinaStatus.PLANEJADA,
            "tema_ids": [str(tema.id)],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
