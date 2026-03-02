from domain.Alerta import Alerta

class AlertaFactory:
    @staticmethod
    def criar_alerta(titulo, mensagem, ocorrencia, escopo, horario):
        if not ocorrencia:
            raise ValueError("Um alerta precisa estar vinculado a uma ocorrência.")
            
        return Alerta(titulo, mensagem, ocorrencia, escopo, horario)