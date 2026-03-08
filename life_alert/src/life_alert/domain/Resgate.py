import datetime

class Resgate:
    _id_auto = 1
    def __init__(self, ocorrencia, dataInicio=None, descricao="", dataFim=None, qtdResgatados=0):
        self.id = Resgate._id_auto
        Resgate._id_auto += 1
        self.ocorrencia = ocorrencia
        self.dataInicio = dataInicio or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.descricao = descricao
        self.dataFim = dataFim
        
        self.qtdResgatados = qtdResgatados

    # Encapsulamento

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
            
            self.qtdResgatados += qtd
            return f"{qtd} vítima(s) adicionada(s) ao resgate com sucesso."
        except ValueError as e:
            raise ValueError(f"Valor inválido: {e}")