"""Schemas for RF-008/RF-033 certificates."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..models.certificado import CertificadoTipo


class CertificadoRead(BaseModel):
    id: UUID
    tipo: CertificadoTipo
    inscricao_id: UUID | None
    tutor_id: UUID | None
    oficina_id: UUID
    hash_validacao: str
    codigo_verificacao: str
    arquivo_pdf_url: str | None
    arquivo_pdf_nome: str | None
    data_emissao: datetime
    carga_horaria_certificada: int | None
    percentual_presenca_certificado: float | None
    revogado: bool

    class Config:
        from_attributes = True


class CertificadoValidacaoRead(BaseModel):
    hash_validacao: str
    codigo_verificacao: str
    tipo: CertificadoTipo
    valido: bool
    participante_nome: str
    participante_tipo: str
    oficina_id: UUID
    oficina_titulo: str
    data_emissao: datetime
    carga_horaria_certificada: int | None
    percentual_presenca_certificado: float | None
    revogado: bool
    motivo_revogacao: str | None

    class Config:
        from_attributes = True