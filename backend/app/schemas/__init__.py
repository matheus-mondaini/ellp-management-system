"""Schema exports."""
from .auth import AuthenticatedUser, LoginRequest, TokenPair, TokenRefreshRequest
from .user import AdminCreate, AlunoCreate, ProfessorCreate, TutorCreate, UserRead
from .tema import TemaCreate, TemaRead, TemaUpdate
from .oficina import OficinaCreate, OficinaRead, OficinaUpdate, TutorAssignmentRead, OficinaSummary
from .professor import ProfessorRead, ProfessorDetailRead
from .inscricao import InscricaoCreate, InscricaoRead, InscricaoStatusUpdate
from .presenca import PresencaBatchCreate, PresencaRead, PresencaRegistro, PresencaUpdate
from .certificado import CertificadoRead, CertificadoValidacaoRead
from .relatorio import (
    RelatorioCertificadosRead,
    RelatorioCertificadosResumo,
    RelatorioFrequenciaAluno,
    RelatorioFrequenciaRead,
    RelatorioFrequenciaResumo,
)

__all__ = [
    "AuthenticatedUser",
    "LoginRequest",
    "TokenPair",
    "TokenRefreshRequest",
    "AdminCreate",
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
    "InscricaoStatusUpdate",
    "PresencaBatchCreate",
    "PresencaRead",
    "PresencaRegistro",
    "PresencaUpdate",
    "CertificadoRead",
    "CertificadoValidacaoRead",
    "RelatorioFrequenciaResumo",
    "RelatorioFrequenciaAluno",
    "RelatorioFrequenciaRead",
    "RelatorioCertificadosResumo",
    "RelatorioCertificadosRead",
]
