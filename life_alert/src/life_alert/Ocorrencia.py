class Ocorrencia:
    def __init__(self, id, atendente, agente, civil, dataHora, status, descricao, local, gravidade, tipo, qtdAfetados):
        self.id = id
        self.atendente = atendente
        self.agente = agente
        self.civil = civil
        self.dataHora = dataHora
        self.status = status
        self.descricao = descricao
        self.local = local
        self.gravidade = gravidade
        self.tipo = tipo
        self.qtdAfetados = qtdAfetados

    def abrirOcorrencia():
        pass

    def atualizarStatus():
        pass

class OcorrenciaPolicial(Ocorrencia):
    def __init__(self, tipoCrime, qtdCriminosos, descricaoSuspeito, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoCrime = tipoCrime
        self.qtdCriminosos = qtdCriminosos
        self.descricaoSuspeito = descricaoSuspeito

    def registrarBoletim():
        pass

class OcorrenciaMedica(Ocorrencia):
    def __init__(self, perfilMedico, sintomas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.perfilMedico = perfilMedico
        self.sintomas = sintomas

    def registrarSintomas():
        pass

    def enviarPerfilmedico():
        pass