"""Participation history aggregation service for RF-013."""
from __future__ import annotations

from typing import Literal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Aluno, Inscricao, Oficina, Professor, Tutor

HistoricoTipo = Literal["aluno", "tutor", "professor"]


def _not_found(tipo: HistoricoTipo) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{tipo.title()} não encontrado")


def historico_aluno(db: Session, aluno_id: UUID) -> dict:
    aluno = db.get(Aluno, aluno_id)
    if not aluno:
        raise _not_found("aluno")

    stmt = (
        select(Inscricao)
        .options(
            selectinload(Inscricao.oficina),
            selectinload(Inscricao.certificado),
        )
        .where(Inscricao.aluno_id == aluno_id)
        .order_by(Inscricao.created_at.desc())
    )
    inscricoes = db.scalars(stmt).all()

    itens = []
    for inscricao in inscricoes:
        oficina = inscricao.oficina
        itens.append(
            {
                "oficina_id": oficina.id,
                "oficina_titulo": oficina.titulo,
                "papel": "aluno",
                "status_oficina": oficina.status,
                "data_inicio": oficina.data_inicio,
                "data_fim": oficina.data_fim,
                "carga_horaria": oficina.carga_horaria,
                "status_inscricao": inscricao.status,
                "percentual_presenca": float(inscricao.percentual_presenca or 0),
                "certificado_emitido": bool(inscricao.certificado),
            }
        )

    return {
        "referencia_tipo": "aluno",
        "referencia_id": aluno.id,
        "total_registros": len(itens),
        "itens": itens,
    }


def historico_tutor(db: Session, tutor_id: UUID) -> dict:
    tutor = db.get(Tutor, tutor_id)
    if not tutor:
        raise _not_found("tutor")

    stmt = (
        select(Oficina)
        .join(Oficina.tutores)
        .where(Tutor.id == tutor_id)
        .order_by(Oficina.data_inicio.desc())
    )
    oficinas = db.scalars(stmt).all()

    itens = []
    for oficina in oficinas:
        itens.append(
            {
                "oficina_id": oficina.id,
                "oficina_titulo": oficina.titulo,
                "papel": "tutor",
                "status_oficina": oficina.status,
                "data_inicio": oficina.data_inicio,
                "data_fim": oficina.data_fim,
                "carga_horaria": oficina.carga_horaria,
                "status_inscricao": None,
                "percentual_presenca": None,
                "certificado_emitido": None,
            }
        )

    return {
        "referencia_tipo": "tutor",
        "referencia_id": tutor.id,
        "total_registros": len(itens),
        "itens": itens,
    }


def historico_professor(db: Session, professor_id: UUID) -> dict:
    professor = db.get(Professor, professor_id)
    if not professor:
        raise _not_found("professor")

    stmt = (
        select(Oficina)
        .where(Oficina.professor_id == professor_id)
        .order_by(Oficina.data_inicio.desc())
    )
    oficinas = db.scalars(stmt).all()

    itens = []
    for oficina in oficinas:
        itens.append(
            {
                "oficina_id": oficina.id,
                "oficina_titulo": oficina.titulo,
                "papel": "professor",
                "status_oficina": oficina.status,
                "data_inicio": oficina.data_inicio,
                "data_fim": oficina.data_fim,
                "carga_horaria": oficina.carga_horaria,
                "status_inscricao": None,
                "percentual_presenca": None,
                "certificado_emitido": None,
            }
        )

    return {
        "referencia_tipo": "professor",
        "referencia_id": professor.id,
        "total_registros": len(itens),
        "itens": itens,
    }
