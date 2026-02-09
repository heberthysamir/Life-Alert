class EquipeResgate:
    _id_auto = 1

    def __init__(self, agentes, localidade, status, setor, especialidade):
        self.id = EquipeResgate._id_auto
        EquipeResgate._id_auto += 1
        self.agentes = agentes if agentes is not None else []
        self.localidade = localidade
        self.status = status
        self.setor = setor
        self.especialidade = especialidade
    
    def __str__(self):
        return f"Equipe {self.id} - {self.especialidade} ({self.setor}) - Status: {self.status}"

    @staticmethod
    def cadastrarEquipe(lista_equipes):
        print("\n--- Cadastro de Nova Equipe de Resgate ---")
        localidade = input("Localidade da base: ")
        setor = input("Setor de atuação (ex.: SAMU, PM, SUS, PRF...): ")
        especialidade = input("Especialidade (ex: Incêndios, Resgate em Altura, Primeiros Socorros): ")
        
        nova_equipe = EquipeResgate(
            agentes=[], 
            localidade=localidade, 
            status="Disponível", 
            setor=setor, 
            especialidade=especialidade
        )
        
        lista_equipes.append(nova_equipe)
        print(f"\nEquipe de {especialidade} (ID: {nova_equipe.id}) cadastrada com sucesso!")
        return nova_equipe

    def adicionarResgate(self, resgate):
        pass

    def removerAgente(self, agente):
        pass

    def atualizarStatus(self, novo_status):
        pass