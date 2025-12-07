"""Security helpers for hashing and JWT handling."""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from ..config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _create_token(*, data: dict[str, Any], expires_minutes: int, secret: str) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire, "iat": now, "jti": str(uuid.uuid4())})
    return jwt.encode(to_encode, secret, algorithm=settings.jwt_algorithm)


def create_access_token(data: dict[str, Any]) -> str:
    return _create_token(
        data=data,
        expires_minutes=settings.jwt_access_token_expires_minutes,
        secret=settings.jwt_secret_key,
    )


def create_refresh_token(data: dict[str, Any]) -> str:
    return _create_token(
        data=data,
        expires_minutes=settings.jwt_refresh_token_expires_minutes,
        secret=settings.jwt_refresh_secret_key,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def decode_refresh_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_refresh_secret_key, algorithms=[settings.jwt_algorithm])


class InvalidTokenError(Exception):
    """Raised when JWT decoding fails."""

    pass


def safe_decode(token: str, *, refresh: bool = False) -> dict[str, Any]:
    try:
        if refresh:
            return decode_refresh_token(token)
        return decode_access_token(token)
    except JWTError as exc:  # pragma: no cover - propagates to caller
        raise InvalidTokenError("invalid token") from exc
