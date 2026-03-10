import datetime

class Atendimento:
    """
    Gerencia o ciclo de vida de um atendimento realizado por um Atendente.
    Registra o tempo de resposta, a urgência e vincula a ocorrência ao 
    processo de triagem antes do resgate.
    """
    def __init__(self, atendente, ocorrencia, civil=None, grauUrgencia="Não definido", relatorio="Não definido", horaInicio=None, horaFinal=None,**kwargs):
        self.id = kwargs.get('id', None)
        self.atendente = atendente
        self.ocorrencia = ocorrencia
        self.civil = civil if civil else ocorrencia.civil
        self._grauUrgencia = None
        self._relatorio = None
        self._horaInicio = None
        self._horaFinal = None
        # Uso dos setters para validação inicial
        self.grauUrgencia = grauUrgencia
        self.relatorio = relatorio
        self.horaInicio = horaInicio
        self.horaFinal = horaFinal

    @property
    def grauUrgencia(self):
        return self._grauUrgencia
    
    @grauUrgencia.setter
    def grauUrgencia(self, valor):
        urgencias_validas = ["baixa", "média", "alta", "Não definido"]
        if isinstance(valor, str):
            valor_lapidado = valor.strip().lower()
            if valor_lapidado not in [u.lower() for u in urgencias_validas]:
                raise ValueError(f"Grau de urgência deve ser um dos seguintes: {', '.join(urgencias_validas)}.")
            mapa = {u.lower(): u for u in urgencias_validas}
            self._grauUrgencia = mapa[valor_lapidado]
        else:
            raise ValueError("Grau de urgência deve ser uma string.")

    @property
    def relatorio(self):
        return self._relatorio
    
    @relatorio.setter
    def relatorio(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Relatório não pode ser vazio.")
        self._relatorio = valor.strip()

    @property
    def horaInicio(self):
        return self._horaInicio
    
    @horaInicio.setter
    def horaInicio(self, valor):
        if valor is None:
            self._horaInicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Hora de início não pode ser vazia.")
            self._horaInicio = valor.strip()

    @property
    def horaFinal(self):
        return self._horaFinal
    
    @horaFinal.setter
    def horaFinal(self, valor):
        if valor is None:
            self._horaFinal = None
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Hora final não pode ser vazia.")
            self._horaFinal = valor.strip()
    
    def finalizarAtendimento(self, lista_atendimentos):
        self.horaFinal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista_atendimentos.append(self)
        print(f"Atendimento finalizado para o civil {self.civil} às {self.horaFinal}.")

    def __str__(self):
        """Representação para exibição em logs."""
        return f"Atendimento #{self.id} | Ocorrência: {self.ocorrencia.id} | Urgência: {self.grauUrgencia}"

    def __repr__(self):
        """Representação técnica para depuração."""
        return f"Atendimento(id={self.id}, atendente='{self.atendente.nome}', urgencia='{self.grauUrgencia}')"