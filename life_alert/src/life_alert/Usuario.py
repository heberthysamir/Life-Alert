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
    
    @staticmethod
    def listarUsuarios(lista_usuarios):
        print("\nUsuários Cadastrados:")
        if not lista_usuarios:
            print("Nenhum usuário cadastrado.")
            return
        for u in lista_usuarios:
            print(u)
    
    @staticmethod
    def criarUsuario(lista_usuarios):
        print("\nCriar Novo Usuário:")
        print("1 - Civil")
        print("2 - Atendente")
        print("3 - Agente")
        opcao = input("Escolha o tipo: ")

        nome = input("Nome: ")
        cpf = input("CPF: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        senha = input("Senha: ")
        usuario = None

        if opcao == "1":
            usuario = Civil(nome, cpf, telefone, email, senha)
            
        elif opcao == "2":
            turno = input("Turno (manha/tarde/noite): ")
            usuario = Atendente(nome, cpf, telefone, email, senha, turno)

        elif opcao == "3":
            cargo = input("Cargo (lider/operacional): ")
            status = True 
            usuario = Agente(nome, cpf, telefone, email, senha, cargo, status)
        
        else:
            print("Opção inválida!")
            return

        if usuario:
            lista_usuarios.append(usuario)
            print(f"\n{usuario.tipo}: {usuario.nome} cadastrado com sucesso!")

    @staticmethod
    def Login(lista_usuarios):
        print("\nLogin Life Alert:")
        if not lista_usuarios:
            print("Nenhum usuário cadastrado.")
            return
        email = input("E-mail: ")
        senha = input("Senha: ")
        for u in lista_usuarios:
            if u.email == email and u.senha == senha:
                print(f"\nBem-vindo, {u.nome}! Login realizado como {u.tipo}.")
                return u 
        print("\nErro: E-mail ou senha incorretos.")
        return None
    
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