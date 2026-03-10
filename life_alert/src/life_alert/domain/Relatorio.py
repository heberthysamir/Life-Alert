from datetime import datetime
from copy import deepcopy

class Relatorio:
    """
    Consolida dados estatísticos de ocorrências em um período específico.
    """
    def __init__(self, data_inicio, data_fim, estatisticas):
        self._data_inicio = None
        self._data_fim = None
        self._estatisticas = None
        self._data_geracao = None
        # Uso dos setters para validação inicial
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.estatisticas = estatisticas
        self._data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")

    @property
    def data_inicio(self):
        return self._data_inicio
    
    @data_inicio.setter
    def data_inicio(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Data de início não pode ser vazia.")
        self._data_inicio = valor.strip()

    @property
    def data_fim(self):
        return self._data_fim
    
    @data_fim.setter
    def data_fim(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Data de fim não pode ser vazia.")
        self._data_fim = valor.strip()

    @property
    def estatisticas(self):
        return deepcopy(self._estatisticas)
    
    @estatisticas.setter
    def estatisticas(self, valor):
        if not isinstance(valor, dict):
            raise ValueError("Estatísticas deve ser um dicionário.")
        campos_obrigatorios = ['total', 'tipos', 'media_atendimento', 'media_resgate']
        for campo in campos_obrigatorios:
            if campo not in valor:
                raise ValueError(f"Estatísticas deve conter o campo '{campo}'.")
        self._estatisticas = deepcopy(valor)

    @property
    def data_geracao(self):
        return self._data_geracao
    
    def __str__(self):
        return f"Relatório: {self.data_inicio} a {self.data_fim} | Total: {self._estatisticas['total']} ocorrências"

    def __repr__(self):
        return f"Relatorio(inicio='{self.data_inicio}', fim='{self.data_fim}', total={self._estatisticas['total']})"