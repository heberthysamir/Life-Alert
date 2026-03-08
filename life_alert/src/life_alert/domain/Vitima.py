class Vitima:
    """Entidade Fraca - Vitima depende de Ocorrencia para existir"""

    def __init__(self, nome, idade, situacao, ocorrencia):
        # Validação obrigatória: ocorrência deve existir e ser válida
        if not ocorrencia:
            raise ValueError("Vítima deve estar vinculada a uma ocorrência válida.")

        # Validação adicional: ocorrência deve ter ID (já estar salva no BD)
        if hasattr(ocorrencia, 'id') and not ocorrencia.id:
            raise ValueError("A ocorrência deve estar salva no banco antes de registrar vítimas.")

        self.nome = nome
        self.idade = idade
        self.ocorrencia = ocorrencia  # Referência obrigatória à entidade forte
        self._situacao = None
        self.situacao = situacao

        # ID composto: será gerado como (ocorrencia_id, sequencial)
        self.id = None

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