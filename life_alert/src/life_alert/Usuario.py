class Usuario:
    _id_auto = 1
    def __init__(self, nome, cpf, telefone, email, senha, tipo):
        self.id = Usuario._id_auto
        Usuario._id_auto += 1
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.tipo = tipo

    def __str__(self):
        return f"[{self.id}] {self.nome} - {self.tipo}"

    def novoUsuario():
        pass

    def atualizarUsuario(self, novo_nome=None, novo_telefone=None, novo_email=None, nova_senha=None):
        if novo_nome: self.nome = novo_nome
        if novo_telefone: self.telefone = novo_telefone
        if novo_email: self.email = novo_email
        if nova_senha: self.senha = nova_senha

    def excluirUsuario(self, lista_usuarios):
        if self in lista_usuarios:
            lista_usuarios.remove(self)
            return True
        return False

    def lerUsuarios():
        pass

    def login():
        pass

class Civil(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Civil")

    def registrarOcorrencia():
        pass

class Atendente(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha, turno):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Atendente")
        self.turno = turno

    def analisarOcorencia():
        pass

    def encaminharResgate():
        pass

    def emitirAlerta():
        pass

class Agente(Usuario):
    def __init__(self, nome, cpf, telefone, email, senha, cargo, status):
        super().__init__(nome, cpf, telefone, email, senha, tipo="Agente")
        self.cargo = cargo
        self.status = status

    def atualizarOcorrencia():
        pass

    def cadastrarEquipe():
        pass

    def removerEquipe():
        pass