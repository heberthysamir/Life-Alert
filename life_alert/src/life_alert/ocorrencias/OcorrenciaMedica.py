from .Ocorrencia import Ocorrencia
class OcorrenciaMedica(Ocorrencia):
    def __init__(self, perfilMedico, sintomas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.perfilMedico = perfilMedico
        self.sintomas = sintomas

    def registrarSintomas(self):
        sintomas = input("Digite os sintomas do paciente: ")
        self.sintomas = sintomas
        print(f"Sintomas registrados para ocorrência médica: {self.sintomas}")

    def enviarPerfilmedico(self):
        perfilMedico = input("Digite o perfil médico do paciente: ")
        self.perfilMedico = perfilMedico
        print(f"Perfil médico enviado para ocorrência médica: {self.perfilMedico}")