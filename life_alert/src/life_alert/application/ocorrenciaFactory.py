from life_alert.domain.ocorrencias.Ocorrencia import Ocorrencia
from life_alert.domain.ocorrencias.OcorrenciaPolicial import OcorrenciaPolicial
from life_alert.domain.ocorrencias.OcorrenciaMedica import OcorrenciaMedica

class OcorrenciaFactory:
    @staticmethod
    def criar(tipo_id, **kwargs):
        if tipo_id == "1":
            return OcorrenciaPolicial(**kwargs)
        
        elif tipo_id == "2":
            return OcorrenciaMedica(**kwargs)
        
        else:
            return Ocorrencia(**kwargs)