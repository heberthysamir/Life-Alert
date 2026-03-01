class Ocorrencia:
    _id_auto = 1
    def __init__(self, atendente, agente, civil, dataHora, status, descricao, rua, bairro, cidade, estado, complemento, gravidade, tipo, qtdAfetados, equipe):
        self.id = Ocorrencia._id_auto
        self.atendente = atendente
        self.agente = agente
        self.civil = civil
        self.dataHora = dataHora
        self.status = status
        self.descricao = descricao
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.complemento = complemento
        self.gravidade = gravidade
        self.tipo = tipo
        self.qtdAfetados = qtdAfetados
        self.equipe = None

    def __str__(self):
        return f"[{self.id}] {self.tipo} - Status: {self.status}\nDescrição: {self.descricao} \nHorário: {self.dataHora}\nGravidade: {self.gravidade}\nQuantidade de afetados: {self.qtdAfetados}\nEndereço: {self.rua},{self.bairro} - {self.complemento}\n"
    
    @staticmethod
    def listarOcorrencias(lista_ocorrencias):
        print("\nOcorrências Registradas:")
        if not lista_ocorrencias:
            print("Nenhuma ocorrência registrada.")
            return
        for o in lista_ocorrencias:
            print(o)