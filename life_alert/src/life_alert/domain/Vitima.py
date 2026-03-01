class Vitima:
    def __init__(self, nome, idade, situacao, ocorrencia):
        self.nome = nome
        self.idade = idade
        self.situacao = situacao
        self.ocorrencia = ocorrencia

    def atualizar_situacao(self, nova_situacao):
        if nova_situacao.strip():
            self.situacao = nova_situacao
            return True
        return False

    def __str__(self):
        oc_id = getattr(self.ocorrencia, 'id', 'N/A')
        return f"Vítima: {self.nome} | Idade: {self.idade} | Situação: {self.situacao} | Ocorrência #{oc_id}"