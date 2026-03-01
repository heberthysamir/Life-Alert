from ocorrencias.Ocorrencia import Ocorrencia
from ocorrencias.OcorrenciaPolicial import OcorrenciaPolicial
from ocorrencias.OcorrenciaMedica import OcorrenciaMedica

class OcorrenciaFactory:
    @staticmethod
    def criar(tipo_id, **kwargs):
        if tipo_id == "1":
            return OcorrenciaPolicial(**kwargs)
        
        elif tipo_id == "2":
            return OcorrenciaMedica(**kwargs)
        
        else:
            return Ocorrencia(**kwargs)