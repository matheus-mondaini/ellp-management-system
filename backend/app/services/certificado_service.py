"""Rules for issuing certificates (RF-008/RF-033)."""
from __future__ import annotations

import secrets
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Certificado, CertificadoTipo, Inscricao, Oficina
from ..models.inscricao import InscricaoStatus

CERTIFICADO_RELATIONS = selectinload(Certificado.inscricao).selectinload(Inscricao.oficina)


def _generate_hash() -> str:
    return uuid4().hex


def _generate_code() -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(10))


def _inscricao_ready(inscricao: Inscricao) -> None:
    if inscricao.status != InscricaoStatus.CONCLUIDO or not inscricao.apto_certificado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inscrição não apta para certificado",
        )


def _ensure_not_exists(db: Session, *, inscricao_id: UUID | None, tutor_id: UUID | None) -> None:
    stmt = select(Certificado.id)
    if inscricao_id:
        stmt = stmt.where(Certificado.inscricao_id == inscricao_id)
    if tutor_id:
        stmt = stmt.where(Certificado.tutor_id == tutor_id)
    if db.execute(stmt).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificado já emitido")


def emitir_para_inscricao(db: Session, inscricao_id: UUID) -> Certificado:
    inscricao = db.get(Inscricao, inscricao_id)
    if not inscricao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")

    _inscricao_ready(inscricao)
    _ensure_not_exists(db, inscricao_id=inscricao_id, tutor_id=None)

    oficina: Oficina = inscricao.oficina
    certificado = Certificado(
        inscricao=inscricao,
        oficina_id=oficina.id,
        tipo=CertificadoTipo.CONCLUSAO_ALUNO,
        hash_validacao=_generate_hash(),
        codigo_verificacao=_generate_code(),
        arquivo_pdf_url=f"https://storage.ellp.dev/certificados/{uuid4().hex}.pdf",
        arquivo_pdf_nome=f"certificado-{inscricao_id}.pdf",
        carga_horaria_certificada=oficina.carga_horaria,
        percentual_presenca_certificado=inscricao.percentual_presenca,
    )
    db.add(certificado)
    db.commit()
    db.refresh(certificado)
    return certificado


def listar(db: Session) -> list[Certificado]:
    stmt = select(Certificado).options(CERTIFICADO_RELATIONS).order_by(Certificado.created_at.desc())
    return db.scalars(stmt).all()


def get_certificado(db: Session, certificado_id: UUID) -> Certificado:
    stmt = select(Certificado).options(CERTIFICADO_RELATIONS).where(Certificado.id == certificado_id)
    certificado = db.scalars(stmt).first()
    if not certificado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificado não encontrado")
    return certificado
