"""
Container de Injeção de Dependências
Centraliza todos os repositórios para facilitar uso na interface
"""

from .usuarioRepository import UsuarioRepository
from .ocorrenciaRepository import OcorrenciaRepository
from .alertaRepository import AlertaRepository
from .atendimentoRepository import AtendimentoRepository
from .equipeRepository import EquipeRepository
from .vitimaRepository import VitimaRepository
from .resgateRepository import ResgateRepository


class RepositoryContainer:
    """Container que centraliza todos os repositórios"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RepositoryContainer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.usuario = UsuarioRepository()
        self.ocorrencia = OcorrenciaRepository()
        self.alerta = AlertaRepository()
        self.atendimento = AtendimentoRepository()
        self.equipe = EquipeRepository()
        self.vitima = VitimaRepository()
        self.resgate = ResgateRepository()
        
        self._initialized = True


def get_repositories():
    """Função helper para obter o container de repositórios"""
    return RepositoryContainer()
