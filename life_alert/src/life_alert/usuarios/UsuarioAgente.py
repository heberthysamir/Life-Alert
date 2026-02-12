from .Usuario import Usuario

class Agente(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha, cargo, status):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Agente")
        self.cargo = cargo
        self.status = status
    
    def exibirMenu(self):
        super().exibirMenu()
        print("3 - Gerenciar Resgate em Andamento")
        print("4 - Cadastrar Vítima")
        if self.cargo.lower() == "lider":
            print("5 - Cadastrar Equipe")
            print("6 - Gerenciar Membros")

    def atualizarOcorrencia():
        pass

    def cadastrarEquipe():
        pass

    def removerEquipe():
        pass
