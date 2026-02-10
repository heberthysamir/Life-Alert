from .Usuario import Usuario
class Atendente(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha, turno):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Atendente")
        self.turno = turno

    def analisarOcorrencia():
        pass

    def encaminharResgate():
        pass

    def emitirAlerta():
        pass