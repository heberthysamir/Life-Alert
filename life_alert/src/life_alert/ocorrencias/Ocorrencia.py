import datetime
from usuarios.UsuarioCivil import Civil
from usuarios.UsuarioAtendente import Atendente
from usuarios.UsuarioAgente import Agente

class Ocorrencia:
    _id_auto = 1
    def __init__(self, atendente, agente, civil, dataHora, status, descricao, rua, bairro, cidade, estado, gravidade, tipo, qtdAfetados):
        self.id = Ocorrencia._id_auto
        self.atendente = atendente
        self.agente = agente
        self.civil = civil
        self.dataHora = dataHora
        self.status = status
        self.descricao = descricao
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.gravidade = gravidade
        self.tipo = tipo
        self.qtdAfetados = qtdAfetados

    def __str__(self):
        return f"[{self.id}] {self.tipo} - {self.descricao} (Status: {self.status})"
    
    @staticmethod
    def listarOcorrencias(lista_ocorrencias):
        print("\nOcorrências Registradas:")
        if not lista_ocorrencias:
            print("Nenhuma ocorrência registrada.")
            return
        for o in lista_ocorrencias:
            print(o)

    @staticmethod
    def abrirOcorrencia(lista_usuarios, usuario_logado):
        from .OcorrenciaMedica import OcorrenciaMedica
        from .OcorrenciaPolicial import OcorrenciaPolicial
        print("\nAbertura de Ocorrência:")
        print("\n1 - Policial")
        print("\n2 - Médica")
        tipo = int(input("\n\nDigite o tipo de ocorrência: "))

        atendente = next((u for u in lista_usuarios if isinstance(u, Atendente)), None)
        agente = next((u for u in lista_usuarios if isinstance(u, Agente)), None)
        civil = usuario_logado if isinstance(usuario_logado, Civil) else None
        if not civil:
             id_civil = input("ID do Civil envolvido (pressione Enter se desconhecido): ")
             if id_civil:
                 civil = next((u for u in lista_usuarios if str(u.id) == id_civil), None)

        dataHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Aberta"
        descricao = input("Descrição da ocorrência: ")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        gravidade = input("Gravidade (baixa/média/alta): ")
        qtdAfetados = int(input("Quantidade de pessoas afetadas: "))

        ocorrencia = None
        
        if tipo == 1:
            tipoCrime = input("Tipo de crime: ")
            qtdCriminosos = int(input("Quantidade de criminosos: "))
            descricaoSuspeito = input("Descrição do suspeito: ")
            ocorrencia = OcorrenciaPolicial(tipoCrime, qtdCriminosos, descricaoSuspeito, atendente, agente, civil, dataHora, status, descricao, rua, bairro, cidade, estado, gravidade, "Policial", qtdAfetados)
        elif tipo == 2:
            perfilMedico = input("Perfil médico: ")
            sintomas = input("Sintomas: ")
            ocorrencia = OcorrenciaMedica(perfilMedico, sintomas, atendente, agente, civil, dataHora, status, descricao, rua, bairro, cidade, estado, gravidade, "Médica", qtdAfetados)
        else:
            ocorrencia = Ocorrencia(atendente, agente, civil, dataHora, None, descricao, rua, bairro, cidade, estado, gravidade, "Desconhecido", qtdAfetados)
            return ocorrencia
    
        if ocorrencia:
            print(f"\nOcorrência do tipo {ocorrencia.tipo} criada com ID {ocorrencia.id}.")
            return ocorrencia
    
        return None