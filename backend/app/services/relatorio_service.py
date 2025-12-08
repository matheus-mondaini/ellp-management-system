"""Relatórios para RF-014 e RF-015."""
from __future__ import annotations

from statistics import fmean
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Aluno, Certificado, Inscricao, Oficina, Pessoa, Tutor
from ..models.certificado import CertificadoTipo

INSCRICAO_RELATIONS = (
    selectinload(Inscricao.aluno)
    .selectinload(Aluno.pessoa)
    .selectinload(Pessoa.user)
)
INSCRICAO_WITH_OFICINA = (
    selectinload(Inscricao.aluno)
    .selectinload(Aluno.pessoa)
    .selectinload(Pessoa.user),
    selectinload(Inscricao.oficina),
)


def _get_oficina_or_404(db: Session, oficina_id: UUID) -> Oficina:
    oficina = db.get(Oficina, oficina_id)
    if not oficina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oficina não encontrada")
    return oficina


def _to_float(value) -> float:
    if value is None:
        return 0.0
    return float(value)


def relatorio_frequencia(db: Session, oficina_id: UUID) -> dict:
    oficina = _get_oficina_or_404(db, oficina_id)
    stmt = (
        select(Inscricao)
        .options(INSCRICAO_RELATIONS)
        .where(Inscricao.oficina_id == oficina_id)
        .order_by(Inscricao.created_at.asc())
    )
    inscricoes = db.scalars(stmt).all()

    totais = len(inscricoes)
    medias = fmean([_to_float(item.percentual_presenca) for item in inscricoes]) if inscricoes else 0.0
    aptos = sum(1 for item in inscricoes if item.apto_certificado)

    return {
        "oficina": oficina,
        "inscricoes": inscricoes,
        "resumo": {
            "total_inscricoes": totais,
            "media_presenca": round(medias, 2) if inscricoes else 0.0,
            "total_aptos_certificado": aptos,
        },
    }


def relatorio_certificados(db: Session) -> dict:
    certificados = db.scalars(
        select(Certificado)
        .options(
            selectinload(Certificado.inscricao)
            .selectinload(Inscricao.aluno)
            .selectinload(Aluno.pessoa)
            .selectinload(Pessoa.user),
            selectinload(Certificado.tutor)
            .selectinload(Tutor.pessoa)
            .selectinload(Pessoa.user),
            selectinload(Certificado.oficina),
        )
        .order_by(Certificado.created_at.desc())
    ).all()

    total_emitidos = len(certificados)
    total_alunos = sum(1 for item in certificados if item.tipo == CertificadoTipo.CONCLUSAO_ALUNO)
    total_tutores = sum(1 for item in certificados if item.tipo == CertificadoTipo.PARTICIPACAO_TUTOR)
    total_revogados = sum(1 for item in certificados if item.revogado)

    pendentes = db.scalars(
        select(Inscricao)
        .options(*INSCRICAO_WITH_OFICINA)
        .where(Inscricao.apto_certificado.is_(True), ~Inscricao.certificado.has())
        .order_by(Inscricao.updated_at.desc())
    ).all()

    return {
        "certificados": certificados,
        "pendentes": pendentes,
        "resumo": {
            "total_emitidos": total_emitidos,
            "total_alunos": total_alunos,
            "total_tutores": total_tutores,
            "total_revogados": total_revogados,
            "pendentes_para_emitir": len(pendentes),
        },
    }
