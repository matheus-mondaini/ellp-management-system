"""Schema exports."""
from .auth import AuthenticatedUser, LoginRequest, TokenPair, TokenRefreshRequest
from .user import AlunoCreate, ProfessorCreate, TutorCreate, UserRead
from .tema import TemaCreate, TemaRead
from .oficina import OficinaCreate, OficinaRead

__all__ = [
    "AuthenticatedUser",
    "LoginRequest",
    "TokenPair",
    "TokenRefreshRequest",
    "AlunoCreate",
    "ProfessorCreate",
    "TutorCreate",
    "UserRead",
    "TemaCreate",
    "TemaRead",
    "OficinaCreate",
    "OficinaRead",
]
