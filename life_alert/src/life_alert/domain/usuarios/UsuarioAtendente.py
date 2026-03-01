from .Usuario import Usuario

class Atendente(Usuario):
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, turno):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Atendente")
        self.turno = turno
    
    def exibirMenu(self):
        super().exibirMenu()
        print("3 - Analisar Ocorrência")
        print("4 - Encaminhar para Resgate")
        print("5 - Emitir Alerta Geral")

    def analisarOcorrencia(self, ocorrencia):
        print(f"\nAnalisando ocorrência: {ocorrencia}")
        print("Vítimas envolvidas:")
        for vitima in ocorrencia.vitimas:
            print(f" - {vitima.nome}")
            print(f"   Idade: {vitima.idade}")
            print(f"   Situação: {vitima.situacao}")

    def encaminharResgate():
        pass

    def emitirAlerta():
        pass

