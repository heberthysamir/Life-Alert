from .Ocorrencia import Ocorrencia
from copy import deepcopy

class OcorrenciaMedica(Ocorrencia):
    """
    Especialização de Ocorrencia para casos de emergência de saúde.
    Adiciona camadas de informações clínicas como sintomas e perfis médicos 
    """
    def __init__(self, perfilMedico=None, sintomas=None, prontuariosVitimas=None, **kwargs):
        super().__init__(**kwargs)
        self._perfilMedico = None
        self._sintomas = None
        # Uso dos setters para validação inicial
        self.perfilMedico = perfilMedico
        self.sintomas = sintomas

    @property
    def perfilMedico(self):
        return self._perfilMedico
    
    @perfilMedico.setter
    def perfilMedico(self, valor):
        if valor is None:
            self._perfilMedico = None
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Perfil médico não pode ser uma string vazia.")
            self._perfilMedico = valor.strip()

    @property
    def sintomas(self):
        return self._sintomas
    
    @sintomas.setter
    def sintomas(self, valor):
        if valor is None:
            self._sintomas = None
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Sintomas não podem ser uma string vazia.")
            self._sintomas = valor.strip()
    
    def __str__(self):
        """Representação para exibição em logs."""
        return f"Ocorrência Médica #{self.id} | Sintomas: {self.sintomas} | Perfil médico: {self.perfilMedico}"
    
    def __repr__(self):
        """Representação técnica para depuração."""
        return f"OcorrenciaMedica(id={self.id}, tipo='{self.tipo}')"
