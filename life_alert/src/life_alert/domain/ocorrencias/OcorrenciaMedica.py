from .Ocorrencia import Ocorrencia

class OcorrenciaMedica(Ocorrencia):
    def __init__(self, *args, **kwargs):
        self.sintomasGerais = kwargs.pop('sintomas', "Não especificado")
        super().__init__(*args, **kwargs)
        self.prontuariosVitimas = {}

    def registrarSintomasVitima(self, vitima, sintomas):
        if vitima not in self.prontuariosVitimas:
            self.prontuariosVitimas[vitima] = {"sintomas": sintomas, "perfilMedico": None}
        else: 
            self.prontuariosVitimas[vitima]["sintomas"] = sintomas
        
        print(f"Sintomas da vítima {vitima.nome} registrados com sucesso!")
    
    def exibirProntuarios(self):
        print("--- Todos os prontuários da ocorrência médica #{self.id} ---")
        if not self.prontuariosVitimas:
            print("No momento, não há prontuários registrados para essa ocorrência.")
            return

        for vitima, dados in self.prontuariosVitimas.items():
            print(f"Vitima: {vitima.nome} (Situação): {vitima.situacao}")
            print(f"    Sintomas relatados: {dados['sintomas']}")
            if dados['perfilMedico']:
                print(f"    {dados['perfilMedico']}")
            else:
                print(f"    Perfil Médico: Não registrado.")

    def registrarPerfilMedico(self, vitima, perfilMedico):
        if vitima not in self.prontuariosVitimas:
            self.prontuariosVitimas[vitima] = {"sintomas": "Não informados", "perfilMedico": perfilMedico}
        else:
            self.prontuariosVitimas[vitima]["perfilMedico"] = perfilMedico
        
        print(f"Perfil Médico vinculado à vítima {vitima.nome} com sucesso!")

    def enviarPerfilmedico(self):
        perfilMedico = input("Digite o perfil médico do paciente: ")
        self.perfilMedico = perfilMedico
        print(f"Perfil médico enviado para ocorrência médica: {self.perfilMedico}")