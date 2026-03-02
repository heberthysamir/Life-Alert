from domain.Relatorio import Relatorio
from datetime import datetime

class RelatorioService:
    @staticmethod
    def gerar_estatisticas(lista_ocorrencias, data_i_str, data_f_str):
        fmt_input = "%d/%m/%Y"
        fmt_oc = "%Y-%m-%d %H:%M:%S" 
        
        d_inicio = datetime.strptime(data_i_str, fmt_input)
        d_fim = datetime.strptime(data_f_str, fmt_input).replace(hour=23, minute=59)

        filtradas = []
        for oc in lista_ocorrencias:
            data_oc = datetime.strptime(oc.dataHora, fmt_oc)
            if d_inicio <= data_oc <= d_fim:
                filtradas.append(oc)

        tipos = {}
        for oc in filtradas:
            tipos[oc.tipo] = tipos.get(oc.tipo, 0) + 1

        tempos_atendimento = []
        for oc in filtradas:
            if hasattr(oc, 'hora_finalizado') and oc.hora_finalizado:
                inicio = datetime.strptime(oc.dataHora, fmt_oc)
                fim = datetime.strptime(oc.hora_finalizado, fmt_oc)
                diff = (fim - inicio).total_seconds() / 60 
                tempos_atendimento.append(diff)

        media_at = round(sum(tempos_atendimento) / len(tempos_atendimento), 1) if tempos_atendimento else 0

        stats = {
            "total": len(filtradas),
            "tipos": tipos,
            "media_atendimento": media_at,
            "media_resgate": 0 
        }
        return Relatorio(data_i_str, data_f_str, stats)