from .Usuario import Usuario

class Civil(Usuario):
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Civil")
        self.perfil_medico = None
    
    def exibirMenu(self):
        super().exibirMenu()
        print("3 - Registrar Ocorrência")
        print("4 - Acompanhar minhas Ocorrências")
        print("5 - Gerenciar Perfil Médico")

    def registrarOcorrencia():
        pass