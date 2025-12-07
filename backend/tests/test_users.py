"""Tests for user management endpoints."""
from fastapi import status


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_manages_admin_profiles(client, admin_user):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    payload = {
        "email": "gestor@ellp.test",
        "password": "Admin456!",
        "nome_completo": "Gestor Projeto",
    }

    create = client.post("/users/admins", headers=headers, json=payload)
    assert create.status_code == status.HTTP_201_CREATED
    data = create.json()
    assert data["role"] == "admin"
    assert data["email"] == payload["email"]

    listing = client.get("/users/admins", headers=headers)
    assert listing.status_code == status.HTTP_200_OK
    emails = [item["email"] for item in listing.json()]
    assert payload["email"] in emails


def test_admin_creates_aluno_success(client, admin_user):
    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.post(
        "/users/alunos",
        headers=headers,
        json={
            "email": "aluno1@ellp.test",
            "password": "Aluno123!",
            "nome_completo": "Aluno Teste",
            "telefone": "43999998888",
            "responsavel_nome": "Responsável",
            "responsavel_telefone": "43988887777",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert payload["email"] == "aluno1@ellp.test"
    assert payload["role"] == "aluno"


def test_professor_cannot_create_tutor(client, professor_user):
    headers = _auth_headers(client, professor_user.email, "prof12345")
    response = client.post(
        "/users/tutores",
        headers=headers,
        json={
            "email": "tutor1@ellp.test",
            "password": "Tutor123!",
            "nome_completo": "Tutor Teste",
            "faculdade": "UTFPR",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_tutor_cannot_access_admin_endpoints(client, tutor_user):
    headers = _auth_headers(client, tutor_user.email, "tutor12345")

    create = client.post(
        "/users/admins",
        headers=headers,
        json={
            "email": "intruso@ellp.test",
            "password": "Tutor123!",
            "nome_completo": "Intruso",
        },
    )
    assert create.status_code == status.HTTP_403_FORBIDDEN

    listing = client.get("/users/admins", headers=headers)
    assert listing.status_code == status.HTTP_403_FORBIDDEN
