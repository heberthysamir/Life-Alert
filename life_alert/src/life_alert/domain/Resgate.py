import datetime

class Resgate:
    _id_auto = 1
    
    def __init__(self, ocorrencia, dataInicio=None, descricao="", dataFim=None, qtdResgatados=0):
        self.id = Resgate._id_auto
        Resgate._id_auto += 1
        self._ocorrencia = None
        self._dataInicio = None
        self._descricao = None
        self._dataFim = None
        self._qtdResgatados = None
        
        self.ocorrencia = ocorrencia
        self.dataInicio = dataInicio
        self.descricao = descricao
        self.dataFim = dataFim
        self.qtdResgatados = qtdResgatados

    @property
    def ocorrencia(self):
        return self._ocorrencia
    
    @ocorrencia.setter
    def ocorrencia(self, valor):
        if valor is None:
            raise ValueError("Ocorrência não pode ser nula.")
        self._ocorrencia = valor

    @property
    def dataInicio(self):
        return self._dataInicio
    
    @dataInicio.setter
    def dataInicio(self, valor):
        if valor is None:
            self._dataInicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Data de início não pode ser vazia.")
            self._dataInicio = valor.strip()

    @property
    def descricao(self):
        return self._descricao
    
    @descricao.setter
    def descricao(self, valor):
        if not isinstance(valor, str):
            raise ValueError("Descrição deve ser uma string.")
        self._descricao = valor.strip()

    @property
    def dataFim(self):
        return self._dataFim
    
    @dataFim.setter
    def dataFim(self, valor):
        if valor is None:
            self._dataFim = None
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Data de fim não pode ser vazia.")
            self._dataFim = valor.strip()

    @property
    def qtdResgatados(self):
        return self._qtdResgatados

    @qtdResgatados.setter
    def qtdResgatados(self, valor):
        try:
            qtd_int = int(valor)
        except (ValueError, TypeError):
            raise ValueError("Quantidade de resgatados deve ser um número inteiro válido.")
            
        if qtd_int < 0:
            raise ValueError("Quantidade de resgatados não pode ser negativa.")
            
        self._qtdResgatados = qtd_int

    def adicionarVitima(self, quantidade):
        try:
            qtd = int(quantidade)
            if qtd < 0:
                raise ValueError("A quantidade de vítimas não pode ser negativa.")
            
            self._qtdResgatados += qtd
            return f"{qtd} vítima(s) adicionada(s) ao resgate com sucesso."
        except ValueError as e:
            raise ValueError(f"Valor inválido: {e}")

    def finalizar_resgate(self, dataFim=None):
        if dataFim is None:
            self.dataFim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.dataFim = dataFim
        return True

    def __str__(self):
        return f"Resgate #{self.id} | Ocorrência: {self.ocorrencia.id} | Resgatados: {self.qtdResgatados} | Início: {self.dataInicio} | Fim: {self.dataFim}"