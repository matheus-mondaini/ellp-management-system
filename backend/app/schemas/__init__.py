"""Schema exports."""
from .auth import AuthenticatedUser, LoginRequest, TokenPair, TokenRefreshRequest
from .user import AlunoCreate, ProfessorCreate, TutorCreate, UserRead
from .tema import TemaCreate, TemaRead, TemaUpdate
from .oficina import OficinaCreate, OficinaRead, OficinaUpdate, TutorAssignmentRead, OficinaSummary
from .professor import ProfessorRead, ProfessorDetailRead
from .inscricao import InscricaoCreate, InscricaoRead

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
    "TemaUpdate",
    "OficinaCreate",
    "OficinaRead",
    "OficinaUpdate",
    "OficinaSummary",
    "TutorAssignmentRead",
    "ProfessorRead",
    "ProfessorDetailRead",
    "InscricaoCreate",
    "InscricaoRead",
]
