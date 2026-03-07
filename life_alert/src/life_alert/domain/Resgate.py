import datetime

class Resgate:
    _id_auto = 1
    def __init__(self, id, ocorrencia, dataInicio, descricao, dataFim, qtdResgatados):
        self.id = Resgate._id_auto
        Resgate._id_auto += 1
        self.ocorrencia = ocorrencia
        self.dataInicio = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.descricao = descricao
        self.dataFim = None
        self.qtdResgatados = 0

    def finalizar(self, relato, total_vitimas):
        self.descricao = relato
        self.qtdResgatados = total_vitimas
        self.dataFim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
