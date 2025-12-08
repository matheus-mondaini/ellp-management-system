"""Endpoints para emissão e download de certificados (RF-008/RF-033)."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import User, UserRole
from ..schemas import CertificadoRead
from ..services import certificado_service
from ._serializers import serialize_certificado

router = APIRouter(prefix="/certificados", tags=["certificados"])
TutorOrHigher = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR, UserRole.TUTOR]))


@router.get("", response_model=list[CertificadoRead])
def listar_certificados(
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> list[CertificadoRead]:
    certificados = certificado_service.listar(db)
    return [serialize_certificado(item) for item in certificados]


@router.post(
    "/inscricoes/{inscricao_id}",
    response_model=CertificadoRead,
    status_code=status.HTTP_201_CREATED,
)
def emitir_certificado_inscricao(
    inscricao_id: UUID,
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> CertificadoRead:
    certificado = certificado_service.emitir_para_inscricao(db, inscricao_id)
    return serialize_certificado(certificado)


@router.get("/{certificado_id}", response_model=CertificadoRead)
def obter_certificado(
    certificado_id: UUID,
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> CertificadoRead:
    certificado = certificado_service.get_certificado(db, certificado_id)
    return serialize_certificado(certificado)


@router.get("/{certificado_id}/download")
def download_certificado(
    certificado_id: UUID,
    db: Session = Depends(get_db),
    _: User = TutorOrHigher,
) -> dict[str, str | None]:
    certificado = certificado_service.get_certificado(db, certificado_id)
    if not certificado.arquivo_pdf_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo PDF ainda não disponível",
        )

    return {
        "arquivo_pdf_url": certificado.arquivo_pdf_url,
        "arquivo_pdf_nome": certificado.arquivo_pdf_nome,
        "hash_validacao": certificado.hash_validacao,
        "codigo_verificacao": certificado.codigo_verificacao,
    }
