"""Application settings powered by pydantic-settings."""
from functools import lru_cache
from typing import Sequence

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration object.

    Defaults are safe for local experimentation only; override through env vars
    or a `.env` file copied from `.env.example`.
    """

    environment: str = "development"
    supabase_url: str = "https://project-id.supabase.co"
    supabase_service_role_key: str = "service-role-key"
    database_url: str = "sqlite:///./ellp.db"

    jwt_secret_key: str = "change-me-access"
    jwt_refresh_secret_key: str = "change-me-refresh"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expires_minutes: int = 30
    jwt_refresh_token_expires_minutes: int = 60 * 24 * 7  # 7 dias
    cors_allowed_origins: Sequence[str] | str = ("http://localhost:3000",)

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def _ensure_sequence(cls, value: Sequence[str] | str) -> Sequence[str]:
        if isinstance(value, str):
            return tuple(origin.strip() for origin in value.split(",") if origin.strip()) or ("*",)
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()
