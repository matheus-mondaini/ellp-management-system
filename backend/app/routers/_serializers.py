"""Helper functions shared across routers."""
from __future__ import annotations

from decimal import Decimal

from ..models import Certificado, Inscricao
from ..schemas import CertificadoRead, CertificadoValidacaoRead, InscricaoRead


def _to_float(value: Decimal | float | int | None) -> float:
    if value is None:
        return 0.0
    return float(value)


def _to_int(value) -> int:
    if value is None:
        return 0
    return int(value)


def serialize_inscricao(inscricao: Inscricao) -> InscricaoRead:
    aluno = inscricao.aluno
    pessoa = aluno.pessoa
    usuario = pessoa.user

    return InscricaoRead(
        id=inscricao.id,
        aluno_id=aluno.id,
        aluno_nome=pessoa.nome_completo,
        aluno_email=usuario.email,
        oficina_id=inscricao.oficina_id,
        status=inscricao.status,
        data_inscricao=inscricao.data_inscricao,
        percentual_presenca=_to_float(inscricao.percentual_presenca),
        total_presencas=_to_int(inscricao.total_presencas),
        total_faltas=_to_int(inscricao.total_faltas),
        total_aulas_previstas=_to_int(inscricao.total_aulas_previstas),
        apto_certificado=bool(inscricao.apto_certificado),
        data_conclusao=inscricao.data_conclusao,
        observacoes=inscricao.observacoes,
    )


def serialize_certificado(certificado: Certificado) -> CertificadoRead:
    return CertificadoRead(
        id=certificado.id,
        tipo=certificado.tipo,
        inscricao_id=certificado.inscricao_id,
        tutor_id=certificado.tutor_id,
        oficina_id=certificado.oficina_id,
        hash_validacao=certificado.hash_validacao,
        codigo_verificacao=certificado.codigo_verificacao,
        arquivo_pdf_url=certificado.arquivo_pdf_url,
        arquivo_pdf_nome=certificado.arquivo_pdf_nome,
        data_emissao=certificado.data_emissao,
        carga_horaria_certificada=certificado.carga_horaria_certificada,
        percentual_presenca_certificado=_to_float(certificado.percentual_presenca_certificado),
        revogado=certificado.revogado,
    )


def serialize_certificado_validacao(certificado: Certificado) -> CertificadoValidacaoRead:
    participante_nome = ""
    participante_tipo = "desconhecido"

    if certificado.inscricao and certificado.inscricao.aluno:
        participante_nome = certificado.inscricao.aluno.pessoa.nome_completo
        participante_tipo = "aluno"
    elif certificado.tutor and certificado.tutor.pessoa:
        participante_nome = certificado.tutor.pessoa.nome_completo
        participante_tipo = "tutor"

    oficina = certificado.oficina or (certificado.inscricao.oficina if certificado.inscricao else None)
    oficina_titulo = oficina.titulo if oficina else ""

    return CertificadoValidacaoRead(
        hash_validacao=certificado.hash_validacao,
        codigo_verificacao=certificado.codigo_verificacao,
        tipo=certificado.tipo,
        valido=not certificado.revogado,
        participante_nome=participante_nome,
        participante_tipo=participante_tipo,
        oficina_id=certificado.oficina_id,
        oficina_titulo=oficina_titulo,
        data_emissao=certificado.data_emissao,
        carga_horaria_certificada=certificado.carga_horaria_certificada,
        percentual_presenca_certificado=_to_float(certificado.percentual_presenca_certificado),
        revogado=certificado.revogado,
        motivo_revogacao=certificado.motivo_revogacao,
    )
