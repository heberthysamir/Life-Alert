import re

class Usuario:
    _id_auto = 1
    _id_lock = False
    
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo):
        self.id = self.__class__._id_auto
        self.__class__._id_auto += 1
        
        self.nome = nome
        self.telefone = telefone
        self.tipo = tipo
        
        self._cpf = None
        self._email = None
        self._senha = None
        self._rua = None
        self._num = None
        self._bairro = None
        self._cidade = None
        self._estado = None
        
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
        return f"[{self.id}] {self.nome} - {self.tipo}."
    
    def obter_funcionalidades(self):
        return [
            ("🔔 Ver Alertas", lambda container: self.gui_ref.tela_central_alertas(container)),
            ("👤 Atualizar Dados", lambda container: self.gui_ref.tela_atualizar_dados(container)),
            ("🗑️ Excluir Conta", lambda container: self.gui_ref.tela_excluir_conta(container))
        ]

    def verificar_senha(self, senha_tentativa):
        if not isinstance(senha_tentativa, str):
            return False
        return self._senha == senha_tentativa
    
    def atualizarUsuario(self, novo_nome=None, novo_telefone=None, novo_email=None, nova_senha=None, nova_rua=None, novo_num=None, novo_bairro=None, nova_cidade=None, novo_estado=None):
        try:
            if novo_nome: 
                self.nome = novo_nome
            if novo_telefone: 
                self.telefone = novo_telefone
            if novo_email: 
                self.email = novo_email
            if nova_senha: 
                self.senha = nova_senha
            if nova_rua: 
                self.rua = nova_rua
            if novo_num: 
                self.num = novo_num
            if novo_bairro: 
                self.bairro = novo_bairro
            if nova_cidade: 
                self.cidade = nova_cidade
            if novo_estado: 
                self.estado = novo_estado
            return True
        except ValueError as e:
            print(f"Erro ao atualizar usuário: {e}")
            return False

    def excluirUsuario(self, lista_usuarios):
        if self in lista_usuarios:
            lista_usuarios.remove(self)
            return True
        return False
