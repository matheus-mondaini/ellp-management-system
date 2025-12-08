"""Dashboard metrics service for RF-022."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Certificado, Inscricao, Oficina
from ..models.inscricao import InscricaoStatus
from ..models.oficina import OficinaStatus

_ACTIVE_STATUSES = (OficinaStatus.INSCRICOES_ABERTAS, OficinaStatus.EM_ANDAMENTO)


def _scalar_count(stmt, db: Session) -> int:
    value = db.scalar(stmt)
    return int(value or 0)


def metricas_gerais(db: Session) -> dict:
    oficinas_ativas = _scalar_count(
        select(func.count()).select_from(Oficina).where(Oficina.status.in_(_ACTIVE_STATUSES)),
        db,
    )
    oficinas_planejadas = _scalar_count(
        select(func.count()).select_from(Oficina).where(Oficina.status == OficinaStatus.PLANEJADA),
        db,
    )
    oficinas_concluidas = _scalar_count(
        select(func.count()).select_from(Oficina).where(Oficina.status == OficinaStatus.CONCLUIDA),
        db,
    )

    total_inscricoes = _scalar_count(select(func.count()).select_from(Inscricao), db)
    inscritos_concluidos = _scalar_count(
        select(func.count()).select_from(Inscricao).where(Inscricao.status == InscricaoStatus.CONCLUIDO),
        db,
    )

    certificados_emitidos = _scalar_count(
        select(func.count()).select_from(Certificado).where(Certificado.revogado.is_(False)),
        db,
    )

    presenca_media = db.scalar(
        select(func.avg(Inscricao.percentual_presenca)).where(Inscricao.percentual_presenca.is_not(None))
    )
    presenca_media = float(presenca_media or 0)

    return {
        "oficinas_ativas": oficinas_ativas,
        "oficinas_planejadas": oficinas_planejadas,
        "oficinas_concluidas": oficinas_concluidas,
        "total_inscricoes": total_inscricoes,
        "inscritos_concluidos": inscritos_concluidos,
        "certificados_emitidos": certificados_emitidos,
        "presenca_media_geral": round(presenca_media, 2),
        "ultima_atualizacao": datetime.now(timezone.utc),
    }
