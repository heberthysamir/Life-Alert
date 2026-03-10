class EquipeResgate:
    """
    Gerencia um grupo de Agentes operacionais destacados para uma localidade.
    Controla a disponibilidade da equipe, sua especialidade (ex: Atendimento Pré-Hospitalar, 
    Combate a Incêndio) e o setor de atuação.
    """
    _id_auto = 1
    def __init__(self, agentes, localidade, status, setor, especialidade,**kwargs):
        self.id = kwargs.get('id', None)
        self.agentes = agentes if agentes is not None else []
        self._localidade = None
        self._status = None
        self._setor = None
        self._especialidade = None
        # Atribuição via setters para validação
        self._agentes = agentes if agentes else []
        self.localidade = localidade
        self.status = status
        self.setor = setor
        self.especialidade = especialidade

    @property
    def agentes(self):
        return self._agentes.copy()
    
    @agentes.setter
    def agentes(self, valor):
        if not isinstance(valor, list):
            raise ValueError("Agentes deve ser uma lista.")
        self._agentes = valor

    @property
    def localidade(self):
        return self._localidade
    
    @localidade.setter
    def localidade(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Localidade não pode ser vazia.")
        self._localidade = valor.strip()

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Status não pode ser vazio.")
        self._status = valor.strip()

    @property
    def setor(self):
        return self._setor
    
    @setor.setter
    def setor(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Setor não pode ser vazio.")
        self._setor = valor.strip()

    @property
    def especialidade(self):
        return self._especialidade
    
    @especialidade.setter
    def especialidade(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Especialidade não pode ser vazia.")
        self._especialidade = valor.strip()
    
    def __str__(self):
        """Representação para exibição em logs."""
        return (f"Equipe #{self.id} | Status: {self.status} | "
                f"Setor: {self.setor} | Especialidade: {self.especialidade} | "
                f"Membros: {self.obter_quantidade_agentes()}")

    def __repr__(self):
        """Representação técnica para depuração."""
        return f"EquipeResgate(id={self.id}, status='{self.status}', especialidade='{self.especialidade}')"