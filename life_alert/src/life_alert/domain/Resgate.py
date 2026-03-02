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

    def adicionarVitima(self, newQtd):
        self.qtdResgatados = newQtd
        return f"Dados atualizados com sucesso! \nQuantidade de resgatados até o momento: {self.qtdResgatados}"


    def concluirResgate(self):  
        self.dataFim = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.ocorrencia.status = "Finalizada"
        return f"Resgate finalizado em {self.dataFim}."
