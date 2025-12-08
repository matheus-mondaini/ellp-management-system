"""Schemas para RF-014/RF-015 (Relatórios)."""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from ..models.inscricao import InscricaoStatus
from .certificado import CertificadoRead
from .inscricao import InscricaoRead


class RelatorioFrequenciaResumo(BaseModel):
    total_inscricoes: int
    media_presenca: float
    total_aptos_certificado: int


class RelatorioFrequenciaAluno(BaseModel):
    inscricao_id: UUID
    aluno_nome: str
    aluno_email: str
    status: InscricaoStatus
    percentual_presenca: float
    total_presencas: int
    total_faltas: int
    apto_certificado: bool


class RelatorioFrequenciaRead(BaseModel):
    oficina_id: UUID
    oficina_titulo: str
    resumo: RelatorioFrequenciaResumo
    alunos: list[RelatorioFrequenciaAluno]


class RelatorioCertificadosResumo(BaseModel):
    total_emitidos: int
    total_alunos: int
    total_tutores: int
    total_revogados: int
    pendentes_para_emitir: int


class RelatorioCertificadosRead(BaseModel):
    resumo: RelatorioCertificadosResumo
    certificados: list[CertificadoRead]
    pendentes: list[InscricaoRead]
