from .Usuario import Usuario
class Civil(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Civil")

    def registrarOcorrencia():
        pass