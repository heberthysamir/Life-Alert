from domain.Vitima import Vitima

class VitimaFactory:
    @staticmethod
    def criar(nome, idade, situacao, ocorrencia):
        """
        Factory para criar vítimas (entidade fraca).
        Valida que a ocorrência existe e é válida antes de criar a vítima.
        """
        if not ocorrencia:
            raise ValueError("Não é possível criar vítima sem uma ocorrência válida.")

        # Validação adicional: ocorrência deve ter ID salvo no BD
        if hasattr(ocorrencia, 'id') and not ocorrencia.id:
            raise ValueError("A ocorrência deve estar salva no banco de dados antes de registrar vítimas.")

        return Vitima(
            nome=nome if nome else "Desconhecido",
            idade=int(idade) if str(idade).isdigit() else 0,
            situacao=situacao if situacao else "Aguardando Triagem",
            ocorrencia=ocorrencia  # Referência obrigatória à entidade forte
        )