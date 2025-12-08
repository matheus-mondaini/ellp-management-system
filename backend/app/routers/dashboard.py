"""Dashboard endpoints for RF-022."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import require_role
from ..models import User, UserRole
from ..schemas import DashboardMetricasRead
from ..services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
AdminOnly = Depends(require_role([UserRole.ADMIN]))


@router.get("/metricas", response_model=DashboardMetricasRead)
def dashboard_metricas(
    db: Session = Depends(get_db),
    _: User = AdminOnly,
) -> DashboardMetricasRead:
    payload = dashboard_service.metricas_gerais(db)
    return DashboardMetricasRead(**payload)
