from .Ocorrencia import Ocorrencia
from copy import deepcopy

class OcorrenciaMedica(Ocorrencia):
    def __init__(self, perfilMedico=None, sintomas=None, prontuariosVitimas=None, **kwargs):
        super().__init__(**kwargs)
        self._perfilMedico = None
        self._sintomas = None
        self._prontuariosVitimas = None
        
        self.perfilMedico = perfilMedico
        self.sintomas = sintomas
        self.prontuariosVitimas = prontuariosVitimas if prontuariosVitimas else {}

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

    @property
    def prontuariosVitimas(self):
        return deepcopy(self._prontuariosVitimas)
    
    @prontuariosVitimas.setter
    def prontuariosVitimas(self, valor):
        if valor is None:
            self._prontuariosVitimas = {}
        elif isinstance(valor, dict):
            self._prontuariosVitimas = deepcopy(valor)
        else:
            raise ValueError("Prontuários deve ser um dicionário.")

    def registrarSintomasVitima(self, vitima, sintomas):
        if not isinstance(sintomas, str) or not sintomas.strip():
            raise ValueError("Sintomas não podem ser vazios.")
        
        if vitima not in self._prontuariosVitimas:
            self._prontuariosVitimas[vitima] = {"sintomas": sintomas.strip(), "perfilMedico": None}
        else: 
            self._prontuariosVitimas[vitima]["sintomas"] = sintomas.strip()
        
        print(f"Sintomas da vítima {vitima.nome} registrados com sucesso!")
        return True
    
    def exibirProntuarios(self):
        print(f"--- Todos os prontuários da ocorrência médica #{self.id} ---")
        if not self._prontuariosVitimas:
            print("No momento, não há prontuários registrados para essa ocorrência.")
            return

        for vitima, dados in self._prontuariosVitimas.items():
            print(f"Vitima: {vitima.nome} (Situação): {vitima.situacao}")
            print(f"    Sintomas relatados: {dados['sintomas']}")
            if dados['perfilMedico']:
                print(f"    {dados['perfilMedico']}")
            else:
                print(f"    Perfil Médico: Não registrado.")

    def registrarPerfilMedico(self, vitima, perfilMedico):
        if vitima not in self._prontuariosVitimas:
            self._prontuariosVitimas[vitima] = {"sintomas": "Não informados", "perfilMedico": perfilMedico}
        else:
            self._prontuariosVitimas[vitima]["perfilMedico"] = perfilMedico
        
        print(f"Perfil Médico vinculado à vítima {vitima.nome} com sucesso!")
        return True

    def enviarPerfilmedico(self):
        perfilMedico = input("Digite o perfil médico do paciente: ")
        try:
            self.perfilMedico = perfilMedico
            print(f"Perfil médico enviado para ocorrência médica: {self.perfilMedico}")
            return True
        except ValueError as e:
            print(f"Erro: {e}")
            return False