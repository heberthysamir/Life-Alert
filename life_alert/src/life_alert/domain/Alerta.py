class Alerta:
    """
    Representa uma notificação de emergência enviada aos usuários.
    O alerta é disparado com base em uma ocorrência ativa e possui um escopo 
    (rua, bairro ou cidade) que define o raio de abrangência da notificação.
    """
    def __init__(self, titulo, mensagem, ocorrencia, escopo, horario):
        self._titulo = None
        self._mensagem = None
        self._ocorrencia = None
        self._escopo = None
        self._horario = None
        # Uso dos setters para validação inicial
        self.titulo = titulo
        self.mensagem = mensagem
        self.ocorrencia = ocorrencia
        self.escopo = escopo
        self.horario = horario

    @property
    def titulo(self):
        return self._titulo
    
    @titulo.setter
    def titulo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Título do alerta não pode ser vazio.")
        self._titulo = valor.strip()

    @property
    def mensagem(self):
        return self._mensagem
    
    @mensagem.setter
    def mensagem(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Mensagem do alerta não pode ser vazia.")
        self._mensagem = valor.strip()

    @property
    def ocorrencia(self):
        return self._ocorrencia
    
    @ocorrencia.setter
    def ocorrencia(self, valor):
        if valor is None:
            raise ValueError("Ocorrência não pode ser nula.")
        self._ocorrencia = valor

    @property
    def escopo(self):
        return self._escopo
    
    @escopo.setter
    def escopo(self, novo_escopo):
        escopos_permitidos = ["cidade", "bairro", "rua"]
        if isinstance(novo_escopo, str) and novo_escopo.strip().lower() in escopos_permitidos:
            self._escopo = novo_escopo.strip().lower()
        else:
            raise ValueError(f"Escopo deve ser um dos seguintes: {', '.join(escopos_permitidos)}.")

    @property
    def horario(self):
        return self._horario
    
    @horario.setter
    def horario(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Horário não pode ser vazio.")
        self._horario = valor.strip()

    def __str__(self):
        """Representação para exibição em logs."""
        return (f"🚨 {self.titulo} ({self.horario})\n"
                f"   Local: {self.ocorrencia.bairro} - {self.ocorrencia.cidade}\n"
                f"   Aviso: {self.mensagem}\n")
    
    def __repr__(self):
        """Representação técnica para depuração."""
        return f"Alerta(id={self.id}, escopo='{self.escopo}', titulo='{self.titulo}')"