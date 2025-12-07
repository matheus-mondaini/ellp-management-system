"""API tests for RF-012 (Gestão de Professores)."""
from fastapi import status


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_tutor_lists_professores(client, tutor_user, professor_entity):
    headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.get("/professores", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert any(item["id"] == str(professor_entity.id) for item in payload)


def test_professor_detail_includes_oficinas(client, tutor_user, professor_entity, oficina):
    headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.get(f"/professores/{professor_entity.id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(professor_entity.id)
    assert data["oficinas"][0]["id"] == str(oficina.id)


def test_aluno_cannot_list_professores(client, aluno_user):
    headers = _auth_headers(client, aluno_user.email, "aluno12345")
    response = client.get("/professores", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
