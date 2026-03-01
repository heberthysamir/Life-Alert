from datetime import datetime
from domain.Relatorio import Relatorio

class RelatorioService:
    @staticmethod
    def gerar_relatorio_por_periodo(lista_ocorrencias, data_inicio_str, data_fim_str):
        fmt = "%d/%m/%Y"
        d_inicio = datetime.strptime(data_inicio_str, fmt)
        d_fim = datetime.strptime(data_fim_str, fmt)
        
        filtradas = []
        for o in lista_ocorrencias:
            data_oc = datetime.strptime(o.dataHora.split()[0], "%Y-%m-%d")
            if d_inicio <= data_oc <= d_fim:
                filtradas.append(o)
        
        stats = {
            "Policiais": len([o for o in filtradas if o.tipo == "Policial"]),
            "Médicas": len([o for o in filtradas if o.tipo == "Médica"]),
            "Finalizadas": len([o for o in filtradas if o.status == "Finalizada"])
        }
        
        return Relatorio(data_inicio_str, data_fim_str, stats, len(filtradas))