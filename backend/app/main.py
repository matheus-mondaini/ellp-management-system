"""Entry point for the FastAPI application used during planning."""
from fastapi import FastAPI

app = FastAPI(title="ELLP Management System API", version="0.1.0")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return basic metadata so CI smoke tests have a deterministic endpoint."""
    return {"status": "ok", "service": "ellp-backend", "version": app.version}
