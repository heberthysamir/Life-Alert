from .Usuario import Usuario

class Civil(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Civil")
    
    def exibirMenu(self):
        super().exibirMenu()
        print("3 - Registrar Ocorrência")
        print("4 - Acompanhar minhas Ocorrências")

    def registrarOcorrencia():
        pass