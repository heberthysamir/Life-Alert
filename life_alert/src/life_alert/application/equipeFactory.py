from domain.EquipeResgate import EquipeResgate

class EquipeFactory:
    """
    Classe responsável pela criação de objetos da classe que ela importa.
    """
    @staticmethod
    def criar_equipe(lider, localidade, setor, especialidade):
        return EquipeResgate(
            agentes=[lider],
            localidade=localidade,
            status="Disponível",
            setor=setor,
            especialidade=especialidade
        )