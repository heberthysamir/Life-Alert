import datetime

class Resgate:
    _id_auto = 1
    def __init__(self, ocorrencia, dataInicio=None, descricao="", dataFim=None, qtdResgatados=0):
        self.id = Resgate._id_auto
        Resgate._id_auto += 1
        self.ocorrencia = ocorrencia
        self.dataInicio = dataInicio or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.descricao = descricao
        self.dataFim = dataFim
        self.qtdResgatados = qtdResgatados

    def finalizar(self, relato, total_vitimas):
        self.descricao = relato
        self.qtdResgatados = total_vitimas
        self.dataFim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")