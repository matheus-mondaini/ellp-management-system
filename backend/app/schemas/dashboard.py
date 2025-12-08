"""Dashboard schemas for RF-022."""
from datetime import datetime

from pydantic import BaseModel, Field


class DashboardMetricasRead(BaseModel):
    oficinas_ativas: int = Field(..., ge=0)
    oficinas_planejadas: int = Field(..., ge=0)
    oficinas_concluidas: int = Field(..., ge=0)
    total_inscricoes: int = Field(..., ge=0)
    inscritos_concluidos: int = Field(..., ge=0)
    certificados_emitidos: int = Field(..., ge=0)
    presenca_media_geral: float = Field(..., ge=0)
    ultima_atualizacao: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "oficinas_ativas": 3,
                "oficinas_planejadas": 1,
                "oficinas_concluidas": 5,
                "total_inscricoes": 120,
                "inscritos_concluidos": 87,
                "certificados_emitidos": 80,
                "presenca_media_geral": 82.5,
                "ultima_atualizacao": "2025-12-08T12:30:00Z",
            }
        }
