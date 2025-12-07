"""ORM entities exported for convenience."""
from .base import Base
from .user import User
from .pessoa import Pessoa
from .aluno import Aluno
from .tutor import Tutor
from .professor import Professor

__all__ = [
    "Base",
    "User",
    "Pessoa",
    "Aluno",
    "Tutor",
    "Professor",
]
