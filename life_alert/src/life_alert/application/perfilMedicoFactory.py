from domain.PerfilMedico import PerfilMedico

class PerfilMedicoFactory:
    @staticmethod
    def criar(alergias, doencas, deficiencia, tipo_sanguineo):
        return PerfilMedico(
            alergias=alergias if alergias else "Nenhuma",
            doencas=doencas if doencas else "Nenhuma",
            deficiencia=deficiencia if deficiencia else "Nenhuma",
            tipoSanguineo=tipo_sanguineo if tipo_sanguineo else "Desconhecido"
        )