from datetime import datetime

class Relatorio:
    def __init__(self, data_inicio, data_fim, estatisticas):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.estatisticas = estatisticas
        self.data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")

    def exibir(self):
        print("\n" + "="*50)
        print(f"📊 RELATÓRIO ESTATÍSTICO: {self.data_inicio} a {self.data_fim}")
        print(f"Gerado em: {self.data_geracao}")
        print("-" * 50)
        
        print(f"🔹 QUANTIDADE TOTAL: {self.estatisticas['total']}")
        print(f"🔹 POR TIPO:")
        for tipo, qtd in self.estatisticas['tipos'].items():
            print(f"   - {tipo}: {qtd}")
        
        print("-" * 50)
        print(f"⏱️ TEMPO MÉDIO DE ATENDIMENTO: {self.estatisticas['media_atendimento']} min")
        print(f"⏱️ TEMPO MÉDIO DE RESGATE:    {self.estatisticas['media_resgate']} min")
        print("="*50 + "\n")