"""Authentication endpoint tests."""
from fastapi import status


def test_login_success(client, admin_user):
    response = client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "admin12345"},
    )

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["refresh_token"]


def test_login_invalid_password(client, admin_user):
    response = client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "wrong"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token_flow(client, admin_user):
    login = client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "admin12345"},
    ).json()

    refresh = client.post(
        "/auth/refresh",
        json={"refresh_token": login["refresh_token"]},
    )

    assert refresh.status_code == status.HTTP_200_OK
    data = refresh.json()
    assert data["access_token"] != login["access_token"]
