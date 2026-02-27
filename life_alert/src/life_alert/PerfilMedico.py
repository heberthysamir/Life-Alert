class PerfilMedico:
    def __init__(self, alergias, doencas, deficiencia, tipoSanguineo):
        self.alergias = alergias
        self.doencas = doencas
        self.deficiencia = deficiencia
        self.tipoSanguineo = tipoSanguineo

    @staticmethod
    def cadastrarPerfil(usuario_civil):
        if usuario_civil.perfil_medico is not None:
            print("\n Você já possui um perfil médico cadastrado.")
            return
        
        print("Cadastro de Perfil Médico:")

        alergias = input("Alergias (ou 'Nenhuma'): ")
        doencas = input ("Doenças (ou 'Nenhuma'): ")
        deficiencia = input ("Deficiências (ou 'Nenhuma'): ")
        tipoSanguineo = input ("Tipo Sanguíneo (ou 'Desconhecido'): ")

        usuario_civil.perfil_medico = PerfilMedico(alergias, doencas, deficiencia, tipoSanguineo)
        print("Perfil Médico cadastrado com sucesso.")

    def atualizarPerfil(self):
        print("Atualização de Perfil Médico:")
        print("Pressione 'enter' para manter as informações")

        nova_alergia = input(f"Alergias atuais ({self.alergias}): ")
        nova_doenca = input(f"Doenças atuais ({self.doencas}): ")
        nova_deficiencia = input(f"Deficiência atual ({self.deficiencia}): ")
        novo_tipo = input(f"Tipo Sanguíneo atual ({self.tipoSanguineo}): ")

        if nova_alergia: self.alergias = nova_alergia
        if nova_doenca: self.doencas = nova_doenca
        if nova_deficiencia: self.deficiencia = nova_deficiencia
        if novo_tipo: self.tipoSanguineo = novo_tipo

        print("\nPerfil médico atualizado.")

    def exibirInformacoes(self):
        print("\nSuas Informações Médicas:")
        print(f"Alergias: {self.alergias}")
        print(f"Doenças Crônicas: {self.doencas}")
        print(f"Deficiência: {self.deficiencia}")
        print(f"Tipo Sanguíneo: {self.tipoSanguineo}")