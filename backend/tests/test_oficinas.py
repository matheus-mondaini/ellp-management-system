"""API tests for RF-003/RF-004 (Cad. e Catálogo de Oficinas)."""
from datetime import date
from uuid import uuid4

from fastapi import status

from app.models import Oficina, Tema
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


def test_tutor_lists_oficinas_with_filters(client, tutor_user, db_session, professor_entity):
    tema_robotica = Tema(nome="Robotica", descricao="Robotica")
    tema_ia = Tema(nome="IA", descricao="Inteligencia Artificial")
    db_session.add_all([tema_robotica, tema_ia])
    db_session.commit()
    db_session.refresh(tema_robotica)
    db_session.refresh(tema_ia)

    abertas = Oficina(
        professor_id=professor_entity.id,
        titulo="Robotica 101",
        carga_horaria=8,
        capacidade_maxima=12,
        data_inicio=date(2025, 6, 1),
        data_fim=date(2025, 6, 10),
        local="UTFPR",
        status=OficinaStatus.INSCRICOES_ABERTAS,
        temas=[tema_robotica],
    )
    planejada = Oficina(
        professor_id=professor_entity.id,
        titulo="IA Kids",
        carga_horaria=8,
        capacidade_maxima=10,
        data_inicio=date(2025, 7, 1),
        data_fim=date(2025, 7, 10),
        local="UTFPR",
        status=OficinaStatus.PLANEJADA,
        temas=[tema_ia],
    )
    db_session.add_all([abertas, planejada])
    db_session.commit()

    headers = _auth_headers(client, tutor_user.email, "tutor12345")
    response = client.get(
        "/oficinas",
        headers=headers,
        params={
            "status": OficinaStatus.INSCRICOES_ABERTAS,
            "tema_id": str(tema_robotica.id),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["titulo"] == "Robotica 101"


def test_list_oficinas_period_filter(client, admin_user, db_session, professor_entity, tema):
    oficina_jan = Oficina(
        professor_id=professor_entity.id,
        titulo="Oficina Janeiro",
        carga_horaria=6,
        capacidade_maxima=10,
        data_inicio=date(2025, 1, 5),
        data_fim=date(2025, 1, 20),
        local="UTFPR",
        status=OficinaStatus.PLANEJADA,
        temas=[tema],
    )
    oficina_mar = Oficina(
        professor_id=professor_entity.id,
        titulo="Oficina Marco",
        carga_horaria=6,
        capacidade_maxima=10,
        data_inicio=date(2025, 3, 5),
        data_fim=date(2025, 3, 20),
        local="UTFPR",
        status=OficinaStatus.PLANEJADA,
        temas=[tema],
    )
    db_session.add_all([oficina_jan, oficina_mar])
    db_session.commit()

    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.get(
        "/oficinas",
        headers=headers,
        params={"data_inicio": "2025-03-01", "data_fim": "2025-03-31"},
    )

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["titulo"] == "Oficina Marco"


def test_aluno_cannot_list_oficinas(client, aluno_user):
    headers = _auth_headers(client, aluno_user.email, "aluno12345")
    response = client.get("/oficinas", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
