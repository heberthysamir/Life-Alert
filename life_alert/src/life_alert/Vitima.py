class Vitima:
    def __init__(self, nome, idade, situacao, ocorrencia):
        self.nome = nome
        self.idade = idade
        self.situacao = situacao
        self.ocorrencia = ocorrencia

    def atualizarSituacao(self):
        print(f"\nSituação atual de {self.nome}: {self.situacao}")
        nova_situacao = input("Informe a nova situação (ou 'Enter' para cancelar): ")
        
        if nova_situacao.strip():
            self.situacao = nova_situacao
            print(f"Situação de {self.nome} atualizada para: '{self.situacao}'!")
        else:
            print("Atualização cancelada.")