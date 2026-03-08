from datetime import datetime
from copy import deepcopy

class Relatorio:
    def __init__(self, data_inicio, data_fim, estatisticas):
        self._data_inicio = None
        self._data_fim = None
        self._estatisticas = None
        self._data_geracao = None
        
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

    def atualizar_data_geracao(self):
        self._data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
        return self._data_geracao

    def obter_total_ocorrencias(self):
        return self._estatisticas.get('total', 0)

    def obter_estatisticas_por_tipo(self):
        return deepcopy(self._estatisticas.get('tipos', {}))

    def obter_media_atendimento(self):
        return self._estatisticas.get('media_atendimento', 0)

    def obter_media_resgate(self):
        return self._estatisticas.get('media_resgate', 0)

    def exibir(self):
        print("\n" + "="*50)
        print(f"📊 RELATÓRIO ESTATÍSTICO: {self._data_inicio} a {self._data_fim}")
        print(f"Gerado em: {self._data_geracao}")
        print("-" * 50)
        
        print(f"🔹 QUANTIDADE TOTAL: {self._estatisticas['total']}")
        print(f"🔹 POR TIPO:")
        for tipo, qtd in self._estatisticas['tipos'].items():
            print(f"   - {tipo}: {qtd}")
        
        print("-" * 50)
        print(f"⏱️ TEMPO MÉDIO DE ATENDIMENTO: {self._estatisticas['media_atendimento']} min")
        print(f"⏱️ TEMPO MÉDIO DE RESGATE:    {self._estatisticas['media_resgate']} min")
        print("="*50 + "\n")
    
    def __str__(self):
        return f"Relatório: {self._data_inicio} a {self._data_fim} | Total: {self._estatisticas['total']} ocorrências"