class Ocorrencia:
    """
    Representa um chamado de emergência no sistema Life Alert.
    
    Gerencia o ciclo de vida desde a abertura pelo Civil até a finalização 
    pela equipe de Resgate, controlando a validade dos estados de atendimento.
    """
    def __init__(self, atendente, agente, civil, dataHora, status, descricao, rua, bairro, cidade, estado, gravidade, tipo, qtdAfetados,**kwargs):
        self.id = kwargs.get('id', None)
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
        """
        Define o status garantindo que ele pertença ao fluxo operacional permitido.
        Levanta ValueError caso o status seja inválido.
        """
        status_permitidos = [
            "Aberta", 
            "Em Atendimento", 
            "Encaminhada para Resgate", 
            "Em Resgate", 
            "Finalizada"
        ]

        # Normalização para evitar erros de digitação (case-insensitive)
        mapa_status = {s.lower(): s for s in status_permitidos}
        status_lapidado = str(novo_status).strip().lower()

        if status_lapidado not in mapa_status:
            raise ValueError(f"Status deve ser um dos seguintes: {', '.join(status_permitidos)}.")

        self._status = mapa_status[status_lapidado]

    def __str__(self):
        """Representação para exibição em logs."""
        return (f"[{self.id}] {self.tipo} - Status: {self.status}\n"
                f"Descrição: {self.descricao}\n"
                f"Horário: {self.dataHora} | Gravidade: {self.gravidade}\n"
                f"Quantidade de afetados: {self.qtdAfetados}\n"
                f"Endereço: {self.rua}, {self.bairro} ({self.cidade}-{self.estado})\n")

    def __repr__(self):
        """Representação técnica para depuração."""
        return f"Ocorrencia(id={self.id}, tipo='{self.tipo}', status='{self.status}')"