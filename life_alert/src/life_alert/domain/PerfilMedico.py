class PerfilMedico:
    def __init__(self, alergias, doencas, deficiencia, tipoSanguineo, contatoEmerg):
        self._alergias = None
        self._doencas = None
        self._deficiencia = None
        self._tipoSanguineo = None
        self._contatoEmerg = None
        
        self.alergias = alergias
        self.doencas = doencas
        self.deficiencia = deficiencia
        self.tipoSanguineo = tipoSanguineo
        self.contatoEmerg = contatoEmerg
    
    @property
    def alergias(self):
        return self._alergias
    
    @alergias.setter
    def alergias(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Campo de alergias não pode ser vazio.")
        self._alergias = valor.strip()
    
    @property
    def doencas(self):
        return self._doencas
    
    @doencas.setter
    def doencas(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Campo de doenças não pode ser vazio.")
        self._doencas = valor.strip()
    
    @property
    def deficiencia(self):
        return self._deficiencia
    
    @deficiencia.setter
    def deficiencia(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Campo de deficiência não pode ser vazio.")
        self._deficiencia = valor.strip()
    
    @property
    def tipoSanguineo(self):
        return self._tipoSanguineo
    
    @tipoSanguineo.setter
    def tipoSanguineo(self, valor):
        tipos_validos = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
        if not isinstance(valor, str):
            raise ValueError("Tipo sanguíneo deve ser uma string.")
        valor_upper = valor.strip().upper()
        if valor_upper not in tipos_validos:
            raise ValueError(f"Tipo sanguíneo inválido. Tipos aceitos: {', '.join(tipos_validos)}")
        self._tipoSanguineo = valor_upper
    
    @property
    def contatoEmerg(self):
        return self._contatoEmerg
    
    @contatoEmerg.setter
    def contatoEmerg(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Contato de emergência não pode ser vazio.")
        self._contatoEmerg = valor.strip()

    def atualizar_dados(self, nova_alergia=None, nova_doenca=None, nova_deficiencia=None, novo_tipo=None, novo_contato=None):
        try:
            if nova_alergia is not None: 
                self.alergias = nova_alergia
            if nova_doenca is not None: 
                self.doencas = nova_doenca
            if nova_deficiencia is not None: 
                self.deficiencia = nova_deficiencia
            if novo_tipo is not None: 
                self.tipoSanguineo = novo_tipo
            if novo_contato is not None:
                self.contatoEmerg = novo_contato
            return True
        except ValueError as e:
            print(f"Erro ao atualizar perfil médico: {e}")
            return False

    def __str__(self):
        return (f"INFORMAÇÕES MÉDICAS:\n"
                f"Alergias: {self.alergias}\n"
                f"Doenças Crônicas: {self.doencas}\n"
                f"Deficiência: {self.deficiencia}\n"
                f"Tipo Sanguíneo: {self.tipoSanguineo}\n"
                f"Contato de Emergência: {self.contatoEmerg}")