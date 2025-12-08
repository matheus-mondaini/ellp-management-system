"""SQLAlchemy engine/session helpers."""
from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from .config import get_settings

settings = get_settings()


def _engine_kwargs(database_url: str) -> dict[str, Any]:
    """Infer engine keyword arguments based on the target database."""

    url = make_url(database_url)
    kwargs: dict[str, Any] = {"future": True, "pool_pre_ping": True}

    if url.drivername.startswith("sqlite"):
        if url.database in {None, ":memory:"}:
            kwargs["connect_args"] = {"check_same_thread": False}
        return kwargs

    host = (url.host or "").lower()
    if host.endswith("supabase.co"):
        connect_args = kwargs.setdefault("connect_args", {})
        connect_args.setdefault("sslmode", "require")
        kwargs.setdefault("pool_size", 5)
        kwargs.setdefault("max_overflow", 5)

    return kwargs


engine = create_engine(settings.database_url, **_engine_kwargs(settings.database_url))
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session per-request."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
