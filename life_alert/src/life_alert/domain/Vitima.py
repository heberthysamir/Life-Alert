class Vitima:
    def __init__(self, nome, idade, situacao, ocorrencia):
        self._nome = None
        self._idade = None
        self._situacao = None
        self._ocorrencia = None
        
        self.nome = nome
        self.idade = idade
        self.situacao = situacao
        self.ocorrencia = ocorrencia

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome da vítima não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def idade(self):
        return self._idade
    
    @idade.setter
    def idade(self, valor):
        try:
            idade_int = int(valor)
        except (ValueError, TypeError):
            raise ValueError("Idade deve ser um número inteiro válido.")
        
        if idade_int < 0 or idade_int > 150:
            raise ValueError("Idade deve estar entre 0 e 150 anos.")
        
        self._idade = idade_int

    @property
    def situacao(self):
        return self._situacao

    @situacao.setter
    def situacao(self, nova_situacao):
        if isinstance(nova_situacao, str) and nova_situacao.strip():
            self._situacao = nova_situacao.strip()
        else:
            raise ValueError("A situação da vítima não pode ser vazia.")

    @property
    def ocorrencia(self):
        return self._ocorrencia
    
    @ocorrencia.setter
    def ocorrencia(self, valor):
        if valor is None:
            raise ValueError("Ocorrência não pode ser nula.")
        self._ocorrencia = valor

    def atualizar_situacao(self, nova_situacao):
        try:
            self.situacao = nova_situacao
            return True
        except ValueError:
            return False

    def __str__(self):
        oc_id = getattr(self.ocorrencia, 'id', 'N/A')
        return f"Vítima: {self.nome} | Idade: {self.idade} | Situação: {self.situacao} | Ocorrência #{oc_id}"