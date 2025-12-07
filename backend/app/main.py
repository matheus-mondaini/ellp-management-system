"""FastAPI entrypoint."""
from fastapi import FastAPI

from .routers import auth, oficinas, professores, temas, users

app = FastAPI(title="ELLP Management System API", version="0.2.0")
app.include_router(auth.router)
app.include_router(oficinas.router)
app.include_router(professores.router)
app.include_router(temas.router)
app.include_router(users.router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return basic metadata so CI smoke tests have a deterministic endpoint."""
    return {"status": "ok", "service": "ellp-backend", "version": app.version}
