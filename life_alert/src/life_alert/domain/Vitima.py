class Vitima:
    def __init__(self, nome, idade, situacao, ocorrencia):
        self.nome = nome
        self.idade = idade
        self.ocorrencia = ocorrencia
        self._situacao = None
        self.situacao = situacao

    # Encapsulamento

    @property
    def situacao(self):
        return self._situacao

    @situacao.setter
    def situacao(self, nova_situacao):
        if isinstance(nova_situacao, str) and nova_situacao.strip():
            self._situacao = nova_situacao.strip()
        else:
            raise ValueError("A situação da vítima não pode ser vazia.")

    def atualizar_situacao(self, nova_situacao):
        try:
            self.situacao = nova_situacao
            return True
        except ValueError:
            return False

    def __str__(self):
        oc_id = getattr(self.ocorrencia, 'id', 'N/A')
        return f"Vítima: {self.nome} | Idade: {self.idade} | Situação: {self.situacao} | Ocorrência #{oc_id}"