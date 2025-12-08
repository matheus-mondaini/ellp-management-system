"""Endpoints para RF-014/RF-015 (Relatórios)."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import Inscricao, User, UserRole
from ..schemas import (
    RelatorioCertificadosRead,
    RelatorioCertificadosResumo,
    RelatorioFrequenciaAluno,
    RelatorioFrequenciaRead,
    RelatorioFrequenciaResumo,
)
from ..services import relatorio_service
from ._serializers import serialize_certificado, serialize_inscricao

router = APIRouter(prefix="/relatorios", tags=["relatorios"])
AdminOrProfessor = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR]))
AdminOnly = Depends(require_role([UserRole.ADMIN]))


def _serialize_frequencia_entries(inscricoes: list[Inscricao]) -> list[RelatorioFrequenciaAluno]:
    entries: list[RelatorioFrequenciaAluno] = []
    for inscricao in inscricoes:
        aluno = inscricao.aluno
        pessoa = aluno.pessoa
        usuario = pessoa.user
        entries.append(
            RelatorioFrequenciaAluno(
                inscricao_id=inscricao.id,
                aluno_nome=pessoa.nome_completo,
                aluno_email=usuario.email,
                status=inscricao.status,
                percentual_presenca=float(inscricao.percentual_presenca or 0),
                total_presencas=int(inscricao.total_presencas or 0),
                total_faltas=int(inscricao.total_faltas or 0),
                apto_certificado=bool(inscricao.apto_certificado),
            )
        )
    return entries


@router.get("/frequencia/{oficina_id}", response_model=RelatorioFrequenciaRead)
def relatorio_frequencia(
    oficina_id: UUID,
    db: Session = Depends(get_db),
    _: User = AdminOrProfessor,
) -> RelatorioFrequenciaRead:
    payload = relatorio_service.relatorio_frequencia(db, oficina_id)
    resumo = RelatorioFrequenciaResumo(**payload["resumo"])
    alunos = _serialize_frequencia_entries(payload["inscricoes"])
    oficina = payload["oficina"]
    return RelatorioFrequenciaRead(
        oficina_id=oficina.id,
        oficina_titulo=oficina.titulo,
        resumo=resumo,
        alunos=alunos,
    )


@router.get("/certificados", response_model=RelatorioCertificadosRead)
def relatorio_certificados(
    db: Session = Depends(get_db),
    _: User = AdminOnly,
) -> RelatorioCertificadosRead:
    payload = relatorio_service.relatorio_certificados(db)
    resumo = RelatorioCertificadosResumo(**payload["resumo"])
    certificados = [serialize_certificado(item) for item in payload["certificados"]]
    pendentes = [serialize_inscricao(item) for item in payload["pendentes"]]
    return RelatorioCertificadosRead(
        resumo=resumo,
        certificados=certificados,
        pendentes=pendentes,
    )
