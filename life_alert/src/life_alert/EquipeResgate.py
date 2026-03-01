class EquipeResgate:
    _id_auto = 1
    def __init__(self, agentes, localidade, status, setor, especialidade):
        self.id = EquipeResgate._id_auto
        EquipeResgate._id_auto += 1
        self.agentes = agentes if agentes else []
        self.localidade = localidade
        self.status = status
        self.setor = setor
        self.especialidade = especialidade

    def adicionar_membro(self, agente):
        if agente in self.agentes:
            raise ValueError(f"O agente {agente.nome} já está nesta equipe.")
        self.agentes.append(agente)

    def remover_membro(self, id_agente):
        agente = next((a for a in self.agentes if a.id == id_agente), None)
        if not agente:
            raise ValueError("Agente não encontrado nesta equipe.")
        self.agentes.remove(agente)

    def alterar_status_agente(self, id_agente, novo_status):
        agente = next((a for a in self.agentes if a.id == id_agente), None)
        if not agente:
            raise ValueError("Agente não encontrado.")
        agente.status = novo_status