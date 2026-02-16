from Alerta import Alerta

class AlertaFactory:
    @staticmethod
    def criar_alerta(**dados):
        # Validação simples: se esquecerem o título ou mensagem, a fábrica impede o erro
        if not dados.get("titulo") or not dados.get("mensagem"):
            raise ValueError("O alerta precisa de título e mensagem!")

        return Alerta(
            titulo=dados.get("titulo"),
            mensagem=dados.get("mensagem"),
            localizacao=dados.get("localizacao"),
            raio_alcance=dados.get("raio", 2.0) # Raio padrão de 2km se não informado
        )