"""Endpoints para emissão e download de certificados (RF-008/RF-033)."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import Pessoa, Tutor, User, UserRole
from ..schemas import CertificadoRead, CertificadoValidacaoRead
from ..services import auditoria_service, certificado_service
from ._serializers import serialize_certificado, serialize_certificado_validacao

router = APIRouter(prefix="/certificados", tags=["certificados"])
TutorOrHigher = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR, UserRole.TUTOR]))
AdminOrProfessor = Depends(require_role([UserRole.ADMIN, UserRole.PROFESSOR]))
AdminOnly = Depends(require_role([UserRole.ADMIN]))
TutorOnly = Depends(require_role([UserRole.TUTOR]))


def _get_tutor_profile(db: Session, current_user: User) -> Tutor:
    stmt = select(Tutor).join(Pessoa).where(Pessoa.user_id == current_user.id)
    tutor = db.scalars(stmt).first()
    if not tutor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil de tutor não encontrado")
    return tutor


@router.get("", response_model=list[CertificadoRead])
def listar_certificados(
    db: Session = Depends(get_db),
    _: User = AdminOrProfessor,
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
    current_user: User = TutorOrHigher,
) -> CertificadoRead:
    certificado = certificado_service.emitir_para_inscricao(db, inscricao_id)
    auditoria_service.registrar_evento(
        db,
        entidade="certificado",
        entidade_id=certificado.id,
        acao="emitido_aluno",
        usuario=current_user,
        detalhes={"inscricao_id": str(inscricao_id)},
    )
    return serialize_certificado(certificado)


@router.post(
    "/oficinas/{oficina_id}/tutores/{tutor_id}",
    response_model=CertificadoRead,
    status_code=status.HTTP_201_CREATED,
)
def emitir_certificado_tutor(
    oficina_id: UUID,
    tutor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = AdminOnly,
) -> CertificadoRead:
    certificado = certificado_service.emitir_para_tutor(db, oficina_id, tutor_id)
    auditoria_service.registrar_evento(
        db,
        entidade="certificado",
        entidade_id=certificado.id,
        acao="emitido_tutor",
        usuario=current_user,
        detalhes={"oficina_id": str(oficina_id), "tutor_id": str(tutor_id)},
    )
    return serialize_certificado(certificado)


@router.get("/{certificado_id}", response_model=CertificadoRead)
def obter_certificado(
    certificado_id: UUID,
    db: Session = Depends(get_db),
    _: User = AdminOrProfessor,
) -> CertificadoRead:
    certificado = certificado_service.get_certificado(db, certificado_id)
    return serialize_certificado(certificado)


@router.get("/tutores/me", response_model=list[CertificadoRead])
def listar_certificados_tutor(
    db: Session = Depends(get_db),
    current_user: User = TutorOnly,
) -> list[CertificadoRead]:
    tutor = _get_tutor_profile(db, current_user)
    certificados = certificado_service.listar_por_tutor(db, tutor.id)
    return [serialize_certificado(item) for item in certificados]


@router.get("/{certificado_id}/download")
def download_certificado(
    certificado_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = TutorOrHigher,
) -> dict[str, str | None]:
    certificado = certificado_service.get_certificado(db, certificado_id)

    if current_user.role == UserRole.TUTOR:
        tutor = _get_tutor_profile(db, current_user)
        if certificado.tutor_id != tutor.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão para este certificado")

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


@router.get(
    "/validar/{hash_certificado}",
    response_model=CertificadoValidacaoRead,
    include_in_schema=True,
)
def validar_certificado(hash_certificado: str, db: Session = Depends(get_db)) -> CertificadoValidacaoRead:
    certificado = certificado_service.get_por_hash(db, hash_certificado)
    return serialize_certificado_validacao(certificado)
