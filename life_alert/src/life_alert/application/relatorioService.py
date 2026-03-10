from domain.Relatorio import Relatorio
from datetime import datetime

class RelatorioService:
    """
    Classe responsável pela lógica dos cálculos 
    e busca de dados estatísticos para gerar relatórios
    """
    @staticmethod
    def gerar_estatisticas(lista_ocorrencias, data_i_str, data_f_str):
        fmt_input = "%d/%m/%Y"
        fmt_oc = "%Y-%m-%d %H:%M:%S" 
        
        try:
            d_inicio = datetime.strptime(data_i_str, fmt_input)
            d_fim = datetime.strptime(data_f_str, fmt_input).replace(hour=23, minute=59, second=59)
        except ValueError:
            return None 

        filtradas = []
        for oc in lista_ocorrencias:
            try:
                dt_str = oc.dataHora if isinstance(oc.dataHora, str) else str(oc.dataHora)
                data_oc = datetime.strptime(dt_str, fmt_oc)
                
                if d_inicio <= data_oc <= d_fim:
                    filtradas.append(oc)
            except:
                continue

        tipos = {}
        tempos_atendimento = []
        for oc in filtradas:
            inicio_str = getattr(oc, 'dataHora', None)
            fim_str = getattr(oc, 'hora_finalizado', None)

            if inicio_str and fim_str and fim_str != "N/A":
                try:
                    inicio = datetime.strptime(inicio_str, fmt_oc)
                    fim = datetime.strptime(fim_str, fmt_oc)
                    
                    diff = (fim - inicio).total_seconds() / 60 

                    if diff > 0:
                        tempos_atendimento.append(diff)
                except Exception as e:
                    print(f"Erro ao processar datas da OC {oc.id}: {e}")
                    continue

        media_at = round(sum(tempos_atendimento) / len(tempos_atendimento), 1) if tempos_atendimento else 0

        stats = {
            "total": len(filtradas),
            "tipos": tipos,
            "media_atendimento": media_at,
            "media_resgate": 0 
        }
        return Relatorio(data_i_str, data_f_str, stats)