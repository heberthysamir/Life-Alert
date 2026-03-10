from life_alert.domain.ocorrencias.Ocorrencia import Ocorrencia
from life_alert.domain.ocorrencias.OcorrenciaPolicial import OcorrenciaPolicial
from life_alert.domain.ocorrencias.OcorrenciaMedica import OcorrenciaMedica

class OcorrenciaFactory:
    """
    Classe responsável pela criação de objetos da classe que ela importa.
    """
    @staticmethod
    def criar(tipo_id, **kwargs):
        if tipo_id == "1":
            return OcorrenciaPolicial(**kwargs)
        
        elif tipo_id == "2":
            return OcorrenciaMedica(**kwargs)
        
        else:
            return Ocorrencia(**kwargs)