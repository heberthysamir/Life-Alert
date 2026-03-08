class EquipeResgate:
    _id_auto = 1
    
    def __init__(self, agentes, localidade, status, setor, especialidade):
        self.id = EquipeResgate._id_auto
        EquipeResgate._id_auto += 1
        self._agentes = []
        self._localidade = None
        self._status = None
        self._setor = None
        self._especialidade = None
        
        self._agentes = agentes if agentes else []
        self.localidade = localidade
        self.status = status
        self.setor = setor
        self.especialidade = especialidade

    @property
    def agentes(self):
        return self._agentes.copy()

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
    def status(self, novo_status):
        status_permitidos = ["Disponível", "Em ocorrência", "Descansando"]
        if isinstance(novo_status, str):
            status_lapidado = novo_status.strip()
            mapa_status = {s: s for s in status_permitidos}
            if status_lapidado not in mapa_status:
                raise ValueError(f"Status deve ser um dos seguintes: {', '.join(status_permitidos)}.")
            self._status = mapa_status[status_lapidado]
        else:
            raise ValueError("Status deve ser uma string.")

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

    def adicionar_membro(self, agente):
        if agente in self._agentes:
            raise ValueError(f"O agente {agente.nome} já está nesta equipe.")
        self._agentes.append(agente)
        return True

    def remover_membro(self, id_agente):
        agente = next((a for a in self._agentes if a.id == id_agente), None)
        if not agente:
            raise ValueError("Agente não encontrado nesta equipe.")
        self._agentes.remove(agente)
        return True

    def alterar_status_agente(self, id_agente, novo_status):
        agente = next((a for a in self._agentes if a.id == id_agente), None)
        if not agente:
            raise ValueError("Agente não encontrado.")
        agente.status = novo_status
        return True
    
    def obter_quantidade_agentes(self):
        return len(self._agentes)
    
    def __str__(self):
        return f"Equipe #{self.id} | Status: {self.status} | Setor: {self.setor} | Especialidade: {self.especialidade} | Agentes: {self.obter_quantidade_agentes()}"