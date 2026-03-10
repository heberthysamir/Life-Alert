from domain.PerfilMedico import PerfilMedico

class PerfilMedicoFactory:
    """
    Classe responsável pela criação de objetos da classe que ela importa.
    """
    @staticmethod
    def criar(alergias, doencas, deficiencia, tipo_sanguineo, contatoEmerg):
        return PerfilMedico(
            alergias = alergias if alergias else "Não cadastrado",
            doencas = doencas if doencas else "Não cadastrado",
            deficiencia = deficiencia if deficiencia else "Não cadastrado",
            tipoSanguineo = tipo_sanguineo if tipo_sanguineo else "Não cadastrado",
            contatoEmerg = contatoEmerg if contatoEmerg else "Não cadastrado"
        )