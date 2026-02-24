class Alerta:
    def __init__(self, titulo, mensagem, ocorrencia, escopo, horario):
        self.titulo = titulo
        self.mensagem = mensagem
        self.ocorrencia = ocorrencia  
        self.escopo = escopo
        self.horario = horario

    def __str__(self):
        return (f"🚨 {self.titulo} ({self.horario})\n"
                f"   Local: {self.ocorrencia.bairro} - {self.ocorrencia.cidade}\n"
                f"   Aviso: {self.mensagem}\n")