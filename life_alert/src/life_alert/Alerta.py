from datetime import datetime

class Alerta:
    def __init__(self, titulo, mensagem, localizacao, raio_alcance):
        self.id = id(self) # Gera um ID único simples
        self.titulo = titulo
        self.mensagem = mensagem
        self.localizacao = localizacao
        self.raio_alcance = raio_alcance
        self.horario = datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        return f"🚨 {self.titulo} ({self.horario})\n   Mensagem: {self.mensagem}"