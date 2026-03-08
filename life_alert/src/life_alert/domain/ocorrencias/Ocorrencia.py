class Ocorrencia:
    _id_auto = 1
    def __init__(self, atendente, agente, civil, dataHora, status, descricao, rua, bairro, cidade, estado, gravidade, tipo, qtdAfetados,**kwargs):
        self.id = Ocorrencia._id_auto
        Ocorrencia._id_auto += 1
        self.atendente = atendente
        self.agente = agente
        self.civil = civil
        self.dataHora = dataHora
        self.descricao = descricao
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.gravidade = gravidade
        self.tipo = tipo
        self.qtdAfetados = qtdAfetados
        self.equipe = None
        
        self.status = status

    # Encapsulamento

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, novo_status):
        status_permitidos = [
            "Aberta", 
            "Em Atendimento", 
            "Encaminhada para Resgate", 
            "Em Resgate", 
            "Finalizada"
        ]

        mapa_status = {s.lower(): s for s in status_permitidos}
        status_lapidado = str(novo_status).strip().lower()

        if status_lapidado not in mapa_status:
            raise ValueError(f"Status deve ser um dos seguintes: {', '.join(status_permitidos)}.")

        self._status = mapa_status[status_lapidado]

    def __str__(self):
        complemento = getattr(self, 'complemento', 'Sem complemento')
        return f"[{self.id}] {self.tipo} - Status: {self.status}\nDescrição: {self.descricao} \nHorário: {self.dataHora}\nGravidade: {self.gravidade}\nQuantidade de afetados: {self.qtdAfetados}\nEndereço: {self.rua},{self.bairro} - {complemento}\n"
    
    @staticmethod
    def listarOcorrencias(lista_ocorrencias):
        print("\nOcorrências Registradas:")
        if not lista_ocorrencias:
            print("Nenhuma ocorrência registrada.")
            return
        for o in lista_ocorrencias:
            print(o)