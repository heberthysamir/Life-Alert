import datetime

class Atendimento:
    _id_auto = 1
    def __init__(self, atendente, ocorrencia, civil=None, grauUrgencia="Não definido", horaInicio=None, horaFinal=None):
        self.id = Atendimento._id_auto
        Atendimento._id_auto += 1
        self.atendente = atendente
        self.ocorrencia = ocorrencia
        self.civil = civil if civil else ocorrencia.civil
        self.grauUrgencia = grauUrgencia
        if horaInicio is None:
            self.horaInicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.horaInicio = horaInicio     
        self.horaFinal = horaFinal

    def __str__(self):
        return f"Atendimento #{self.id} | Status: {self.ocorrencia.status} | Urgência: {self.grauUrgencia} | Local: {self.ocorrencia.bairro}"

    @staticmethod
    def iniciarAtendimento(lista_usuarios, lista_ocorrencia, usuario_logado):
        print("\nAtendimento Iniciado:")

        ocorrencias_abertas = [o for o in lista_ocorrencia if o.status == "Aberta"]

        if not ocorrencias_abertas:
            print("Nenhuma ocorrência aberta.")
            return None
        
        print("\nOcorrências Abertas:")
        for o in ocorrencias_abertas:
            print(f"[{o.id}] {o.tipo} - {o.descricao} (Status: {o.status})")

        id_ocorrencia = input("Digite o ID da ocorrência a ser atendida: ")
        ocorrencia = next((o for o in ocorrencias_abertas if str(o.id) == id_ocorrencia), None)
        if not ocorrencia:
            print("ID de ocorrência inválido.")
            return None
        if ocorrencia.status != "Aberta":
            print("A ocorrência selecionada não está mais aberta.")
            return None
        
        grauUrgencia = input("Grau de urgência (baixa/média/alta): ")
        horaInicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        atendimento = Atendimento(atendente=usuario_logado, civil=ocorrencia.civil, grauUrgencia=grauUrgencia, horaInicio=horaInicio, horaFinal=None, ocorrencia=ocorrencia)
        ocorrencia.status = "Em Atendimento"
        ocorrencia.atendente = usuario_logado

        print(f"\nAtendimento iniciado para {ocorrencia.civil} com grau de urgência {grauUrgencia}.")
        return atendimento
    
    def atualizarAtendimento(self):
        print(f"\nATUALIZANDO ATENDIMENTO:{self.id}")
        print("\nDETALHES DA OCORRÊNCIA:")
        print(self.ocorrencia)
        print(f"Ocorrência: {self.ocorrencia.tipo} | Descrição: {self.ocorrencia.descricao}")
        novo_grau = input("Defina o grau de urgência (baixa/média/alta): ")
        self.grauUrgencia = novo_grau
        print("✅ Dados do atendimento atualizados com sucesso!")

    def encaminharResgate():
        pass

    def finalizarAtendimento(self, lista_atendimentos):
        self.horaFinal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista_atendimentos.append(self)
        print(f"Atendimento finalizado para o civil {self.civil} às {self.horaFinal}.")