"""ORM entities exported for convenience."""
from .base import Base
from .user import User, UserRole
from .pessoa import Pessoa
from .aluno import Aluno
from .tutor import Tutor
from .professor import Professor
from .tema import Tema
from .oficina import Oficina, OficinaStatus
from .inscricao import Inscricao, InscricaoStatus

__all__ = [
    "Base",
    "User",
    "UserRole",
    "Pessoa",
    "Aluno",
    "Tutor",
    "Professor",
    "Tema",
    "Oficina",
    "OficinaStatus",
    "Inscricao",
    "InscricaoStatus",
]
