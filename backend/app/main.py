"""FastAPI entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import (
    auditorias,
    auth,
    certificados,
    dashboard,
    historicos,
    inscricoes,
    oficinas,
    presencas,
    professores,
    relatorios,
    temas,
    users,
)


def create_app() -> FastAPI:
    """Instantiate FastAPI app with every router wired."""
    application = FastAPI(title="ELLP Management System API", version="0.2.0")
    settings = get_settings()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(auth.router)
    application.include_router(certificados.router)
    application.include_router(dashboard.router)
    application.include_router(historicos.router)
    application.include_router(auditorias.router)
    application.include_router(inscricoes.router)
    application.include_router(oficinas.router)
    application.include_router(presencas.router)
    application.include_router(professores.router)
    application.include_router(relatorios.router)
    application.include_router(temas.router)
    application.include_router(users.router)

    @application.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        """Return basic metadata so CI smoke tests have a deterministic endpoint."""
        return {
            "status": "ok",
            "service": "ellp-backend",
            "version": application.version,
        }

    return application


app = create_app()
