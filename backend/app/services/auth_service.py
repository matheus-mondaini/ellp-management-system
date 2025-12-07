"""Business logic for authentication flows."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import AuthenticatedUser, LoginRequest, TokenPair, TokenRefreshRequest
from ..utils import (
    InvalidTokenError,
    create_access_token,
    create_refresh_token,
    safe_decode,
    verify_password,
)


def _get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def _build_token_pair(user: User) -> TokenPair:
    payload = {"sub": str(user.id), "role": user.role}
    access = create_access_token(payload)
    refresh = create_refresh_token(payload)
    return TokenPair(
        access_token=access,
        refresh_token=refresh,
        expires_in=1800,
    )


def login(db: Session, payload: LoginRequest) -> TokenPair:
    user = _get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário desativado")

    user.ultimo_login = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return _build_token_pair(user)


def refresh(db: Session, payload: TokenRefreshRequest) -> TokenPair:
    try:
        data = safe_decode(payload.refresh_token, refresh=True)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido") from exc

    user_id = data.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.get(User, uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário desativado")

    return _build_token_pair(user)


def get_authenticated_user(user: User) -> AuthenticatedUser:
    nome = user.pessoa.nome_completo if user.pessoa else ""
    return AuthenticatedUser(
        id=user.id,
        email=user.email,
        role=user.role,
        nome_completo=nome,
        ativo=user.ativo,
        ultimo_login=user.ultimo_login,
    )
