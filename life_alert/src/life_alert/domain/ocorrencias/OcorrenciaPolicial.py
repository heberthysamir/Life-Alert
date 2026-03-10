from .Ocorrencia import Ocorrencia

class OcorrenciaPolicial(Ocorrencia):
    """
    Especialização de Ocorrencia para incidentes de segurança pública.
    Adiciona campos específicos para investigação preliminar, como o tipo de crime,
    a contagem de envolvidos e a descrição de suspeitos para auxílio às autoridades.
    """
    def __init__(self, tipoCrime, qtdCriminosos, descricaoSuspeito, **kwargs):
        super().__init__(**kwargs)
        self._tipoCrime = None
        self._qtdCriminosos = None
        self._descricaoSuspeito = None
        # Uso dos setters para validação inicial
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

    def __str__(self):
        """Representação para exibição em logs."""
        return f"Ocorrência Policial #{self.id} | Crime: {self.tipoCrime} | Criminosos: {self.qtdCriminosos}"

    def __repr__(self):
        """Representação técnica para depuração."""
        return f"OcorrenciaPolicial(id={self.id}, crime='{self.tipoCrime}', qtd={self.qtdCriminosos})"