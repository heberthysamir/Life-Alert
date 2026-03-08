from .Ocorrencia import Ocorrencia

class OcorrenciaPolicial(Ocorrencia):
    def __init__(self, tipoCrime, qtdCriminosos, descricaoSuspeito, **kwargs):
        super().__init__(**kwargs)
        self._tipoCrime = None
        self._qtdCriminosos = None
        self._descricaoSuspeito = None
        
        self.tipoCrime = tipoCrime
        self.qtdCriminosos = qtdCriminosos
        self.descricaoSuspeito = descricaoSuspeito

    @property
    def tipoCrime(self):
        return self._tipoCrime
    
    @tipoCrime.setter
    def tipoCrime(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Tipo de crime não pode ser vazio.")
        self._tipoCrime = valor.strip()

    @property
    def qtdCriminosos(self):
        return self._qtdCriminosos
    
    @qtdCriminosos.setter
    def qtdCriminosos(self, valor):
        try:
            qtd_int = int(valor)
        except (ValueError, TypeError):
            raise ValueError("Quantidade de criminosos deve ser um número inteiro válido.")
        
        if qtd_int < 0:
            raise ValueError("Quantidade de criminosos não pode ser negativa.")
        
        self._qtdCriminosos = qtd_int

    @property
    def descricaoSuspeito(self):
        return self._descricaoSuspeito
    
    @descricaoSuspeito.setter
    def descricaoSuspeito(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Descrição de suspeito não pode ser vazia.")
        self._descricaoSuspeito = valor.strip()

    def registrarBoletim(self):
        print(f"Boletim registrado para ocorrência policial: {self.tipoCrime}")
        print(f"  - Quantidade de criminosos: {self.qtdCriminosos}")
        print(f"  - Descrição: {self.descricaoSuspeito}")
        return True

    def atualizar_quantidade_criminosos(self, nova_quantidade):
        try:
            self.qtdCriminosos = nova_quantidade
            return True
        except ValueError as e:
            print(f"Erro ao atualizar quantidade: {e}")
            return False

    def __str__(self):
        return f"Ocorrência Policial #{self.id} | Crime: {self.tipoCrime} | Criminosos: {self.qtdCriminosos}"