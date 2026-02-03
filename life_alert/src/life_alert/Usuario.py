class Usuario:
    def __init__(self, id, nome, cpf, telefone, email, senha, tipo):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.tipo = tipo

    def novoUsuario():
        pass

    def atualizarUsuario():
        pass

    def excluirUsuario():
        pass

    def lerUsuarios():
        pass

    def login():
        pass

class Civil(Usuario):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def registrarOcorrencia():
        pass

class Atendente(Usuario):
    def __init__(self, equipe, turno, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.equipe = equipe
        self.turno = turno

    def analisarOcorencia():
        pass

    def encaminharResgate():
        pass

    def emitirAlerta():
        pass

class Agente(Usuario):
    def __init__(self, cargo, funcao, status, equipeResgate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cargo = cargo
        self.funcao = funcao
        self.status = status
        self.equipeResgate = equipeResgate

    def atualizarOcorrencia():
        pass

    def cadastrarEquipe():
        pass

    def removerEquipe():
        pass