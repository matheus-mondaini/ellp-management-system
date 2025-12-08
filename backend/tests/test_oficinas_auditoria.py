"""Audit-related tests for the oficinas router."""
from fastapi import status


def _auth_headers(client, email, password):
    token = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_oficina_emits_audit_event(monkeypatch, client, admin_user, professor_entity, tema):
    audit_calls = []

    def _fake_registrar_evento(db, **kwargs):
        audit_calls.append(kwargs)
        return None

    monkeypatch.setattr(
        "app.routers.oficinas.auditoria_service.registrar_evento",
        _fake_registrar_evento,
    )

    headers = _auth_headers(client, admin_user.email, "admin12345")
    payload = {
        "professor_id": str(professor_entity.id),
        "titulo": "Oficina Auditoria",
        "descricao": "Validando logs",
        "carga_horaria": 4,
        "capacidade_maxima": 8,
        "data_inicio": "2025-01-10",
        "data_fim": "2025-01-20",
        "local": "UTFPR",
        "status": "planejada",
        "tema_ids": [str(tema.id)],
    }

    response = client.post("/oficinas", headers=headers, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert audit_calls, "Evento de auditoria não registrado"
    evento = audit_calls[-1]
    assert evento["recurso"] == "oficina"
    assert evento["acao"] == "criada"
    assert evento["payload"]["titulo"] == payload["titulo"]


def test_assign_tutor_emits_audit_event(monkeypatch, client, admin_user, tutor_entity, oficina):
    audit_calls = []

    def _fake_registrar_evento(db, **kwargs):
        audit_calls.append(kwargs)
        return None

    monkeypatch.setattr(
        "app.routers.oficinas.auditoria_service.registrar_evento",
        _fake_registrar_evento,
    )

    headers = _auth_headers(client, admin_user.email, "admin12345")
    response = client.post(
        f"/oficinas/{oficina.id}/tutores/{tutor_entity.id}",
        headers=headers,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert audit_calls, "Evento de auditoria não registrado"
    evento = audit_calls[-1]
    assert evento["recurso"] == "oficina_tutor"
    assert evento["acao"] == "associado"
    assert evento["payload"] == {"tutor_id": str(tutor_entity.id)}


def test_create_inscricao_emits_audit_event(
    monkeypatch,
    client,
    admin_user,
    oficina,
    aluno_entity,
):
    audit_calls = []

    def _fake_registrar_evento(db, **kwargs):
        audit_calls.append(kwargs)
        return None

    monkeypatch.setattr(
        "app.routers.oficinas.auditoria_service.registrar_evento",
        _fake_registrar_evento,
    )

    headers = _auth_headers(client, admin_user.email, "admin12345")
    payload = {"aluno_id": str(aluno_entity.id)}
    response = client.post(
        f"/oficinas/{oficina.id}/inscricoes",
        headers=headers,
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert audit_calls, "Evento de auditoria não registrado"
    evento = audit_calls[-1]
    assert evento["recurso"] == "inscricao"
    assert evento["acao"] == "criada"
    assert evento["payload"] == {"oficina_id": str(oficina.id), "aluno_id": payload["aluno_id"]}
