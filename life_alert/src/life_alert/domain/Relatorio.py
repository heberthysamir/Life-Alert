from datetime import datetime

class Relatorio:
    def __init__(self, data_inicio, data_fim, estatisticas, total_ocorrencias):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.estatisticas = estatisticas  
        self.total_ocorrencias = total_ocorrencias
        self.data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")

    def exibir(self):
        print("\n" + "="*40)
        print(f"📋 RELATÓRIO DE PERÍODO: {self.data_inicio} a {self.data_fim}")
        print(f"Gerado em: {self.data_geracao}")
        print("-"*40)
        for chave, valor in self.estatisticas.items():
            print(f"{chave}: {valor}")
        print(f"\nTOTAL GERAL: {self.total_ocorrencias}")
        print("="*40 + "\n")
        