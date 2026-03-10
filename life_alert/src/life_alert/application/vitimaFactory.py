from domain.Vitima import Vitima

class VitimaFactory:
    """
    Classe responsável pela criação de objetos da classe que ela importa.
    """
    @staticmethod
    def criar(nome, idade, situacao, ocorrencia):
        if not ocorrencia:
            raise ValueError("Não é possível criar vítima sem uma ocorrência válida.")

        if hasattr(ocorrencia, 'id') and not ocorrencia.id:
            raise ValueError("A ocorrência deve estar salva no banco de dados antes de registrar vítimas.")

        return Vitima(
            nome=nome if nome else "Desconhecido",
            idade=int(idade) if str(idade).isdigit() else 0,
            situacao=situacao if situacao else "Aguardando Triagem",
            ocorrencia=ocorrencia  
        )