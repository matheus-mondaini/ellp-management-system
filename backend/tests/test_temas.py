"""Tests for Tema management endpoints."""
from fastapi import status

from app.models import Tema


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_professor_lists_temas_sorted(client, db_session, professor_user):
    temas = [
        Tema(nome="Zoologia", descricao="Animais"),
        Tema(nome="Astronomia", descricao="Espaco"),
        Tema(nome="Biologia", descricao="Vida"),
    ]
    db_session.add_all(temas)
    db_session.commit()

    headers = _auth_headers(client, professor_user.email, "prof12345")
    response = client.get("/temas", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    names = [item["nome"] for item in payload]
    assert names == sorted(names)


def test_admin_creates_tema_success(client, admin_user):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.post(
        "/temas",
        headers=headers,
        json={"nome": "Robotica", "descricao": "Workshops de robotica"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert payload["nome"] == "Robotica"
    assert payload["descricao"] == "Workshops de robotica"
    assert payload["ativo"] is True


def test_create_tema_conflict_returns_409(client, admin_user, tema):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.post(
        "/temas",
        headers=headers,
        json={"nome": tema.nome, "descricao": "Duplicado"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_admin_updates_tema(client, admin_user, tema):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.patch(
        f"/temas/{tema.id}",
        headers=headers,
        json={"descricao": "Nova descricao", "ativo": False},
    )

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["descricao"] == "Nova descricao"
    assert payload["ativo"] is False


def test_admin_deletes_tema(client, admin_user, tema):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.delete(f"/temas/{tema.id}", headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    fetch = client.get(f"/temas/{tema.id}", headers=headers)
    assert fetch.status_code == status.HTTP_404_NOT_FOUND


def test_aluno_cannot_access_temas(client, aluno_user):
    headers = _auth_headers(client, aluno_user.email, "aluno12345")
    response = client.get("/temas", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
