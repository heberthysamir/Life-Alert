import re

class Usuario:
    """
    Classe base para a hierarquia de usuários do sistema Life Alert.
    Gerencia dados pessoais, validações de segurança (CPF, Email, Senha) 
    e persistência básica de localização.
    """
    _id_auto = 1
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo):
        self.id = Usuario._id_auto
        Usuario._id_auto += 1
        # validações básicas para encapsulamento
        if not nome:
            raise ValueError("Nome é obrigatório")
        if not cpf:
            raise ValueError("CPF é obrigatório")
        if not email:
            raise ValueError("E-mail é obrigatório")
        if not senha:
            raise ValueError("Senha é obrigatória")

        self.nome = nome
        self.telefone = telefone
        self.tipo = tipo
        # Atributos privados para os @property
        self._cpf = None
        self._email = None
        self._senha = None
        self._rua = None
        self._num = None
        self._bairro = None
        self._cidade = None
        self._estado = None
        # Uso dos setters para validação inicial
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.rua = rua
        self.num = num
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
    
    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("CPF não pode ser vazio.")
        self._cpf = value.strip()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Email não pode ser vazio.")
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value.strip()):
            raise ValueError("Email inválido.")
        self._email = value.strip().lower()
    
    @property
    def senha(self):
        raise AttributeError("Acesso à senha não é permitido.")
    
    @senha.setter
    def senha(self, value):
        if not isinstance(value, str) or len(value) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres.")
        self._senha = value
    
    @property
    def rua(self):
        return self._rua
    
    @rua.setter
    def rua(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Rua não pode ser vazia.")
        self._rua = value.strip()
    
    @property
    def num(self):
        return self._num
    
    @num.setter
    def num(self, value):
        if not isinstance(value, (str, int)) or str(value).strip() == "":
            raise ValueError("Número não pode ser vazio.")
        self._num = str(value).strip()
    
    @property
    def bairro(self):
        return self._bairro
    
    @bairro.setter
    def bairro(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Bairro não pode ser vazio.")
        self._bairro = value.strip()
    
    @property
    def cidade(self):
        return self._cidade
    
    @cidade.setter
    def cidade(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Cidade não pode ser vazia.")
        self._cidade = value.strip()
    
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Estado não pode ser vazio.")
        self._estado = value.strip()

    def __str__(self):
        id_str = self.id if self.id else "Novo"
        return f"[{id_str}] {self.nome} - {self.tipo}."  
      
    def obter_funcionalidades(self):
        """Retorna as ações disponíveis para este usuário na interface."""
        return [
            ("🔔 Ver Alertas", lambda container: self.gui_ref.tela_central_alertas(container)),
            ("👤 Atualizar Dados", lambda container: self.gui_ref.tela_atualizar_dados(container)),
            ("🗑️ Excluir Conta", lambda container: self.gui_ref.tela_excluir_conta(container))
        ]

    
    @staticmethod
    def login(lista_usuarios, email, senha):
        """
        Método de classe para autenticação.
        Retorna o objeto Usuario se as credenciais forem válidas.
        """
        email_busca = email.strip().lower()
        for u in lista_usuarios:
            if u.email == email_busca and u.verificar_senha(senha):
                return u
        return None
    
    def atualizarUsuario(self, novo_nome=None, novo_telefone=None, novo_email=None, nova_senha=None, nova_rua=None, novo_num=None, novo_bairro=None, nova_cidade=None, novo_estado=None):
        """
        Atualiza os campos fornecidos dinamicamente.
        Exemplo: usuario.atualizarUsuario(novo_nome="João")
        """
        if novo_nome: self.nome = novo_nome
        if novo_telefone: self.telefone = novo_telefone
        if novo_email: self.email = novo_email
        if nova_senha: self.senha = nova_senha

        if nova_rua: self.rua = nova_rua
        if novo_num: self.num = novo_num
        if novo_bairro: self.bairro = novo_bairro
        if nova_cidade: self.cidade = nova_cidade
        if novo_estado: self.estado = novo_estado

    def __str__(self):
        """Representação para exibição em logs."""
        id_display = self.id if self.id else "Novo"
        return f"[{id_display}] {self.nome} ({self.tipo})"

    def __repr__(self):
        """Representação técnica para depuração."""
        return f"Usuario(nome='{self.nome}', email='{self.email}', tipo='{self.tipo}')"