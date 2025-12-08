"""API tests for RF-013 (Histórico de Participação)."""
from uuid import UUID, uuid4

from fastapi import status

from app.models import Certificado, Inscricao
from app.models.certificado import CertificadoTipo
from app.models.inscricao import InscricaoStatus


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


def test_admin_consulta_historico_aluno(client, db_session, admin_user, oficina, aluno_entity):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    inscricao_id = _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)

    registro = db_session.get(Inscricao, UUID(inscricao_id))
    registro.status = InscricaoStatus.CONCLUIDO
    registro.percentual_presenca = 90
    db_session.add(
        Certificado(
            inscricao_id=registro.id,
            oficina_id=registro.oficina_id,
            tipo=CertificadoTipo.CONCLUSAO_ALUNO,
            hash_validacao=f"hash-{uuid4().hex}",
            codigo_verificacao=f"cod-{uuid4().hex[:10]}",
        )
    )
    db_session.commit()

    response = client.get(f"/historicos/alunos/{aluno_entity.id}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["referencia_tipo"] == "aluno"
    assert payload["total_registros"] == 1
    item = payload["itens"][0]
    assert item["oficina_id"] == str(oficina.id)
    assert item["certificado_emitido"] is True
    assert item["percentual_presenca"] == 90.0


def test_aluno_somente_seu_historico(client, aluno_user, aluno_entity, second_aluno_entity, admin_user, oficina):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    _criar_inscricao(client, admin_headers, oficina.id, aluno_entity.id)
    aluno_headers = _auth_headers(client, aluno_user.email, "aluno12345")

    own = client.get(f"/historicos/alunos/{aluno_entity.id}", headers=aluno_headers)
    assert own.status_code == status.HTTP_200_OK

    forbidden = client.get(f"/historicos/alunos/{second_aluno_entity.id}", headers=aluno_headers)
    assert forbidden.status_code == status.HTTP_403_FORBIDDEN


def test_tutor_historico_e_professor_historico(
    client,
    db_session,
    admin_user,
    tutor_user,
    tutor_entity,
    professor_user,
    professor_entity,
    oficina,
):
    admin_headers = _auth_headers(client, admin_user.email, "admin12345")
    instructor_headers = _auth_headers(client, tutor_user.email, "tutor12345")
    professor_headers = _auth_headers(client, professor_user.email, "prof12345")

    oficina.tutores.append(tutor_entity)
    db_session.commit()

    tutor_resp = client.get(f"/historicos/tutores/{tutor_entity.id}", headers=instructor_headers)
    assert tutor_resp.status_code == status.HTTP_200_OK
    assert tutor_resp.json()["total_registros"] == 1

    prof_resp = client.get(
        f"/historicos/professores/{professor_entity.id}",
        headers=professor_headers,
    )
    assert prof_resp.status_code == status.HTTP_200_OK
    assert prof_resp.json()["total_registros"] >= 1

    # Admin can also query tutor history without restriction
    admin_resp = client.get(f"/historicos/tutores/{tutor_entity.id}", headers=admin_headers)
    assert admin_resp.status_code == status.HTTP_200_OK