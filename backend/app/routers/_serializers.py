"""Helper functions shared across routers."""
from __future__ import annotations

from decimal import Decimal

from ..models import Certificado, Inscricao
from ..schemas import CertificadoRead, InscricaoRead


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
    percentual = certificado.percentual_presenca_certificado
    if isinstance(percentual, Decimal):
        percentual = float(percentual)

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
        percentual_presenca_certificado=percentual,
        revogado=certificado.revogado,
    )
