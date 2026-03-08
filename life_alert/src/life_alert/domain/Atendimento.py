import datetime

class Atendimento:
    _id_auto = 1
    
    def __init__(self, atendente, ocorrencia, civil=None, grauUrgencia="Não definido", relatorio="Não definido", horaInicio=None, horaFinal=None):
        self.id = Atendimento._id_auto
        Atendimento._id_auto += 1
        self.atendente = atendente
        self.ocorrencia = ocorrencia
        self.civil = civil if civil else ocorrencia.civil
        self._grauUrgencia = None
        self._relatorio = None
        self._horaInicio = None
        self._horaFinal = None
        
        self.grauUrgencia = grauUrgencia
        self.relatorio = relatorio
        self.horaInicio = horaInicio
        self.horaFinal = horaFinal

    @property
    def grauUrgencia(self):
        return self._grauUrgencia
    
    @grauUrgencia.setter
    def grauUrgencia(self, valor):
        urgencias_validas = ["baixa", "média", "alta", "Não definido"]
        if isinstance(valor, str):
            valor_lapidado = valor.strip().lower()
            if valor_lapidado not in [u.lower() for u in urgencias_validas]:
                raise ValueError(f"Grau de urgência deve ser um dos seguintes: {', '.join(urgencias_validas)}.")
            mapa = {u.lower(): u for u in urgencias_validas}
            self._grauUrgencia = mapa[valor_lapidado]
        else:
            raise ValueError("Grau de urgência deve ser uma string.")

    @property
    def relatorio(self):
        return self._relatorio
    
    @relatorio.setter
    def relatorio(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Relatório não pode ser vazio.")
        self._relatorio = valor.strip()

    @property
    def horaInicio(self):
        return self._horaInicio
    
    @horaInicio.setter
    def horaInicio(self, valor):
        if valor is None:
            self._horaInicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Hora de início não pode ser vazia.")
            self._horaInicio = valor.strip()

    @property
    def horaFinal(self):
        return self._horaFinal
    
    @horaFinal.setter
    def horaFinal(self, valor):
        if valor is None:
            self._horaFinal = None
        else:
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Hora final não pode ser vazia.")
            self._horaFinal = valor.strip()

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
        
        try:
            atendimento = Atendimento(atendente=usuario_logado, civil=ocorrencia.civil, grauUrgencia=grauUrgencia, horaInicio=horaInicio, horaFinal=None, ocorrencia=ocorrencia)
            ocorrencia.status = "Em Atendimento"
            ocorrencia.atendente = usuario_logado
            print(f"\nAtendimento iniciado para {ocorrencia.civil} com grau de urgência {grauUrgencia}.")
            return atendimento
        except ValueError as e:
            print(f"Erro ao iniciar atendimento: {e}")
            return None
    
    def atualizarAtendimento(self):
        print(f"\nATUALIZANDO ATENDIMENTO:{self.id}")
        print("\nDETALHES DA OCORRÊNCIA:")
        print(self.ocorrencia)
        print(f"Ocorrência: {self.ocorrencia.tipo} | Descrição: {self.ocorrencia.descricao}")
        novo_grau = input("Defina o grau de urgência (baixa/média/alta): ")
        try:
            self.grauUrgencia = novo_grau
            print("✅ Dados do atendimento atualizados com sucesso!")
            return True
        except ValueError as e:
            print(f"Erro: {e}")
            return False

    def alterarUrgencia(self):
        print(f"\nALTERANDO URGÊNCIA DO ATENDIMENTO #{self.id}")
        print(f"Urgência atual: {self.grauUrgencia}")
        novo_grau = input("Defina o novo grau de urgência (baixa/média/alta): ")
        try:
            self.grauUrgencia = novo_grau
            print("✅ Grau de urgência atualizado com sucesso!")
            return True
        except ValueError as e:
            print(f"Erro: {e}")
            return False

    def encerrarAtendimento(self):
        self.horaFinal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.ocorrencia:
            self.ocorrencia.status = "Finalizada"

    @staticmethod
    def listarAtendimentos(lista_atendimentos):
        print("\nAtendimentos Realizados:")
        if not lista_atendimentos:
            print("Nenhum atendimento realizado.")
            return
        for a in lista_atendimentos:
            print(f"[{a.id}] Civil: {a.civil} - Atendente: {a.atendente} - Grau de Urgência: {a.grauUrgencia} - Início: {a.horaInicio} - Fim: {a.horaFinal} - Ocorrência: {a.ocorrencia.descricao}")

    @staticmethod
    def encaminharResgate(lista_equipes, lista_ocorrencia):
        print("\nEncaminhamento para Equipe de Resgate:")

        equipes_disponiveis = [e for e in lista_equipes if any(a.status == "Disponível" for a in e.agentes)]
        ocorrencias_em_atendimento = [o for o in lista_ocorrencia if o.status == "Em Atendimento"]

        if not ocorrencias_em_atendimento:
            print("Nenhuma ocorrência em atendimento.")
            return False

        if not equipes_disponiveis:
            print("Nenhuma equipe de resgate disponível no momento.")
            return False
        
        print("\nOcorrências em Atendimento:")
        for o in ocorrencias_em_atendimento:
            print(f"[{o.id}] {o.tipo} - {o.descricao} (Status: {o.status})")

        id_ocorrencia = input("Digite o ID da ocorrência a ser encaminhada: ")
        ocorrencia = next((o for o in ocorrencias_em_atendimento if str(o.id) == id_ocorrencia), None)
        if not ocorrencia:
            print("ID de ocorrência inválido.")
            return False

        print("\nEquipes de Resgate Disponíveis:")
        for e in equipes_disponiveis:
            print(f"[{e.id}] - {len(e.agentes)} membros")

        id_equipe = input("Digite o ID da equipe de resgate a ser encaminhada: ")
        equipe = next((e for e in equipes_disponiveis if str(e.id) == id_equipe), None)
        if not equipe:
            print("ID de equipe inválido.")
            return False
        
        for agente in equipe.agentes:
            agente.status = "Em ocorrência"

        equipe.status = "Em ocorrência"
        equipes_disponiveis.remove(equipe)

        ocorrencia.equipe = equipe
        ocorrencia.status = "Encaminhada para Resgate"
        print(f"\nOcorrência encaminhada para a equipe {equipe.id}.")
        return True

    def finalizarAtendimento(self, lista_atendimentos):
        self.horaFinal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista_atendimentos.append(self)
        print(f"Atendimento finalizado para o civil {self.civil} às {self.horaFinal}.")