"""Auth endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..middlewares import get_current_user
from ..schemas import AuthenticatedUser, LoginRequest, TokenPair, TokenRefreshRequest
from ..services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    return auth_service.login(db, payload)


@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(payload: TokenRefreshRequest, db: Session = Depends(get_db)) -> TokenPair:
    return auth_service.refresh(db, payload)


@router.get("/me", response_model=AuthenticatedUser)
def me(current_user=Depends(get_current_user)) -> AuthenticatedUser:  # type: ignore[override]
    return auth_service.get_authenticated_user(current_user)
