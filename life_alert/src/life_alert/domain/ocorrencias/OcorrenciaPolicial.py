from .Ocorrencia import Ocorrencia
class OcorrenciaPolicial(Ocorrencia):
    def __init__(self, tipoCrime, qtdCriminosos, descricaoSuspeito, **kwargs):
        super().__init__(**kwargs)
        self.tipoCrime = tipoCrime
        self.qtdCriminosos = qtdCriminosos
        self.descricaoSuspeito = descricaoSuspeito

    def registrarBoletim(self):
        print(f"Boletim registrado para ocorrência policial: {self.tipoCrime}")