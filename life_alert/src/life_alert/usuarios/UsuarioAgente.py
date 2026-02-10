from .Usuario import Usuario
class Agente(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha, cargo, status):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Agente")
        self.cargo = cargo
        self.status = status

    def atualizarOcorrencia():
        pass

    def cadastrarEquipe():
        pass

    def removerEquipe():
        pass