from domain.Vitima import Vitima

class VitimaFactory:
    @staticmethod
    def criar(nome, idade, situacao, ocorrencia):
        return Vitima(
            nome=nome if nome else "Desconhecido",
            idade=int(idade) if str(idade).isdigit() else 0,
            situacao=situacao if situacao else "Aguardando Triagem",
            ocorrencia=ocorrencia
        )