"""Helper functions shared across routers."""
from __future__ import annotations

from decimal import Decimal

from ..models import Inscricao
from ..schemas import InscricaoRead


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
