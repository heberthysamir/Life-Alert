class PerfilMedico:
    def __init__(self, alergias, doencas, deficiencia, tipoSanguineo):
        self.alergias = alergias
        self.doencas = doencas
        self.deficiencia = deficiencia
        self.tipoSanguineo = tipoSanguineo

    def atualizar_dados(self, nova_alergia=None, nova_doenca=None, nova_deficiencia=None, novo_tipo=None):
        """Atualiza apenas os campos que forem passados"""
        if nova_alergia: self.alergias = nova_alergia
        if nova_doenca: self.doencas = nova_doenca
        if nova_deficiencia: self.deficiencia = nova_deficiencia
        if novo_tipo: self.tipoSanguineo = novo_tipo

    def __str__(self):
        return (f"INFORMAÇÕES MÉDICAS:\n"
                f"Alergias: {self.alergias}\n"
                f"Doenças Crônicas: {self.doencas}\n"
                f"Deficiência: {self.deficiencia}\n"
                f"Tipo Sanguíneo: {self.tipoSanguineo}")