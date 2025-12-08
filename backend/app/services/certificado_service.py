"""Rules for issuing certificates (RF-008/RF-033)."""
from __future__ import annotations

import logging
import secrets
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Aluno, Certificado, CertificadoTipo, Inscricao, Oficina, Tutor
from ..models.inscricao import InscricaoStatus
from ..models.oficina import OficinaStatus
from ..utils import (
    formatar_cpf,
    formatar_periodo,
    gerar_certificado_aluno,
    gerar_certificado_tutor,
    upload_pdf_certificado,
)

logger = logging.getLogger(__name__)

CERTIFICADO_RELATIONS = [
    selectinload(Certificado.inscricao).selectinload(Inscricao.oficina),
    selectinload(Certificado.inscricao).selectinload(Inscricao.aluno).selectinload(Aluno.pessoa),
    selectinload(Certificado.tutor).selectinload(Tutor.pessoa),
    selectinload(Certificado.oficina),
]


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


def _ensure_not_exists(
    db: Session,
    *,
    inscricao_id: UUID | None,
    tutor_id: UUID | None,
    oficina_id: UUID | None = None,
) -> None:
    stmt = select(Certificado.id)
    if inscricao_id:
        stmt = stmt.where(Certificado.inscricao_id == inscricao_id)
    if tutor_id:
        stmt = stmt.where(Certificado.tutor_id == tutor_id)
    if oficina_id:
        stmt = stmt.where(Certificado.oficina_id == oficina_id)
    if db.execute(stmt).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificado já emitido")


def _get_oficina_or_404(db: Session, oficina_id: UUID) -> Oficina:
    oficina = db.get(Oficina, oficina_id)
    if not oficina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oficina não encontrada")
    return oficina


def _get_tutor_or_404(db: Session, tutor_id: UUID) -> Tutor:
    tutor = db.get(Tutor, tutor_id)
    if not tutor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tutor não encontrado")
    return tutor


def _ensure_tutor_assigned(oficina: Oficina, tutor: Tutor) -> None:
    if not any(existing.id == tutor.id for existing in oficina.tutores):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tutor não vinculado à oficina",
        )


def emitir_para_inscricao(db: Session, inscricao_id: UUID) -> Certificado:
    inscricao = db.get(Inscricao, inscricao_id)
    if not inscricao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")

    _inscricao_ready(inscricao)
    _ensure_not_exists(db, inscricao_id=inscricao_id, tutor_id=None)

    oficina: Oficina = inscricao.oficina
    aluno: Aluno = inscricao.aluno

    hash_validacao = _generate_hash()
    codigo_verificacao = _generate_code()

    try:
        pdf_bytes = gerar_certificado_aluno(
            nome_aluno=aluno.pessoa.nome_completo,
            cpf_aluno=formatar_cpf(aluno.pessoa.cpf),
            titulo_oficina=oficina.titulo,
            carga_horaria=oficina.carga_horaria,
            periodo=formatar_periodo(str(oficina.data_inicio), str(oficina.data_fim)),
            percentual_presenca=inscricao.percentual_presenca,
            hash_validacao=hash_validacao,
            codigo_verificacao=codigo_verificacao,
        )

        filename = f"aluno-{inscricao_id}.pdf"
        pdf_url = upload_pdf_certificado(pdf_bytes, filename, folder="certificados")
        
    except Exception as e:
        logger.error(f"Erro ao gerar/upload PDF: {e}")
        filename = f"aluno-{inscricao_id}.pdf"
        pdf_url = f"https://storage.dev/certificados/{filename}"
    
    certificado = Certificado(
        inscricao=inscricao,
        oficina_id=oficina.id,
        tipo=CertificadoTipo.CONCLUSAO_ALUNO,
        hash_validacao=hash_validacao,
        codigo_verificacao=codigo_verificacao,
        arquivo_pdf_url=pdf_url,
        arquivo_pdf_nome=filename,
        carga_horaria_certificada=oficina.carga_horaria,
        percentual_presenca_certificado=inscricao.percentual_presenca,
    )
    db.add(certificado)
    db.commit()
    db.refresh(certificado)
    return certificado


def emitir_para_tutor(db: Session, oficina_id: UUID, tutor_id: UUID) -> Certificado:
    oficina = _get_oficina_or_404(db, oficina_id)
    tutor = _get_tutor_or_404(db, tutor_id)

    if oficina.status != OficinaStatus.CONCLUIDA:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Oficina precisa estar concluída",
        )

    _ensure_tutor_assigned(oficina, tutor)
    _ensure_not_exists(db, inscricao_id=None, tutor_id=tutor_id, oficina_id=oficina_id)

    hash_validacao = _generate_hash()
    codigo_verificacao = _generate_code()

    try:
        pdf_bytes = gerar_certificado_tutor(
            nome_tutor=tutor.pessoa.nome_completo,
            cpf_tutor=formatar_cpf(tutor.pessoa.cpf),
            titulo_oficina=oficina.titulo,
            carga_horaria=oficina.carga_horaria,
            periodo=formatar_periodo(str(oficina.data_inicio), str(oficina.data_fim)),
            hash_validacao=hash_validacao,
            codigo_verificacao=codigo_verificacao,
        )

        filename = f"tutor-{tutor_id}-{oficina_id}.pdf"
        pdf_url = upload_pdf_certificado(pdf_bytes, filename, folder="certificados/tutores")
        
    except Exception as e:
        logger.error(f"Erro ao gerar/upload PDF tutor: {e}")
        filename = f"tutor-{tutor_id}-{oficina_id}.pdf"
        pdf_url = f"https://storage.dev/certificados/tutores/{filename}"

    certificado = Certificado(
        tutor_id=tutor.id,
        oficina_id=oficina.id,
        tipo=CertificadoTipo.PARTICIPACAO_TUTOR,
        hash_validacao=hash_validacao,
        codigo_verificacao=codigo_verificacao,
        arquivo_pdf_url=pdf_url,
        arquivo_pdf_nome=filename,
        carga_horaria_certificada=oficina.carga_horaria,
    )
    db.add(certificado)
    db.commit()
    db.refresh(certificado)
    return certificado


def listar(db: Session) -> list[Certificado]:
    stmt = select(Certificado).options(*CERTIFICADO_RELATIONS).order_by(Certificado.created_at.desc())
    return db.scalars(stmt).all()


def listar_por_tutor(db: Session, tutor_id: UUID) -> list[Certificado]:
    stmt = (
        select(Certificado)
        .options(*CERTIFICADO_RELATIONS)
        .where(Certificado.tutor_id == tutor_id)
        .order_by(Certificado.created_at.desc())
    )
    return db.scalars(stmt).all()


def get_certificado(db: Session, certificado_id: UUID) -> Certificado:
    stmt = select(Certificado).options(*CERTIFICADO_RELATIONS).where(Certificado.id == certificado_id)
    certificado = db.scalars(stmt).first()
    if not certificado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificado não encontrado")
    return certificado


def get_por_hash(db: Session, hash_validacao: str) -> Certificado:
    stmt = (
        select(Certificado)
        .options(*CERTIFICADO_RELATIONS)
        .where(Certificado.hash_validacao == hash_validacao)
    )
    certificado = db.scalars(stmt).first()
    if not certificado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificado não encontrado")
    return certificado
