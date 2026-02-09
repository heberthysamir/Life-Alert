from Usuario import Agente

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
    
    def listarMembros(self):
        print(f"Membros da equipe {self.id}:\n")
        if not self.agentes:
            print("Não há agentes nessa equipe.")
            return
        for agente in self.agentes:
            print(f"ID - {agente.id} / Nome - {agente.nome} / Status - {agente.status} / Posição - {agente.cargo}")
        return True

    def adicionarMembro(self, lista_usuarios):
        print("Inserir membro agente na equipe:\n")
        agentes = [u for u in lista_usuarios if isinstance(u, Agente) and u not in self.agentes]

        if not agentes:
            print("Não há membros disponíveis para inserir na equipe no momento.")
            return

        print("Lista de agentes disponíveis: \n")
        for c in agentes:
            print(f"[{c.id}] {c.nome} ({c.cargo})")
        
        idNovoMembro = input ("Digite o ID do agente que deseja inserir na equipe:\n")
        agenteEscolhido = next((a for a in agentes if str(a.id) == idNovoMembro), None)

        if agenteEscolhido:
            self.agentes.append(agenteEscolhido)
            print(f"Agente {agenteEscolhido.nome} agora faz parte da equipe!")
        else:
            print("ID inválido.")
    
    def removerMembro(self):
        print("Remover membro da equipe:\n")
        if not self.listarMembros():
            return
        
        idAgente = int(input("Insira o ID do membro que deseja remover da equipe:\n"))
        agente = next((a for a in self.agentes if self(a.id) == idAgente), None)

        if agente:
            self.agentes.remove(agente)
            print(f"Agente {agente.nome} não faz mais parte da equipe.\n")

        else:
            print("Membro selecionado não se encontra nessa equipe.")
    
    def atualizarStatusMembro(self):
        print(f"Atualizar situação de um membro da equipe: ")
        if not self.listarMembros():
            return

        idAgente = input("Digite o ID do membro da equipe:")
        agente = next((a for a in self.agentes if str(a.id) == idAgente), None)

        if agente:
            print(f"Status atual do membro: {agente.status}")
            novoStatus = input("Novo Status do membro: (ex.: Disponível, Em ocorrência, Ferido...)")
            if novoStatus:
                agente.status = novoStatus
        else:
            print("Membro não se encontra na equipe selecionada.")


    @staticmethod
    def cadastrarEquipe(lista_equipes, usuario_logado):
        print("\nInserir nova equipe:")
        localidade = input("Localidade da base: ")
        setor = input("Setor de atuação (ex.: SAMU, PM, SUS, PRF...): ")
        especialidade = input("Especialidade (ex.: Incêndios, Resgate em Altura, Primeiros Socorros): ")
        
        nova_equipe = EquipeResgate(
            [usuario_logado],
            localidade, 
            "Disponível", 
            setor, 
            especialidade
        )
        
        lista_equipes.append(nova_equipe)
        print(f"\nEquipe de {especialidade} (ID: {nova_equipe.id}) cadastrada com sucesso!")
        return nova_equipe
    
    @staticmethod
    def listarEquipes(lista_equipes):
        print("Equipes cadastradas:")
        if not lista_equipes:
            print("Nenhuma equipe cadastrada.\n")
            return
        
        for equipe in lista_equipes:
            print(equipe)
    
    
