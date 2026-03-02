
class Usuario:
    _id_auto = 1
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo):
        self.id = Usuario._id_auto
        Usuario._id_auto += 1
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.rua = rua
        self.num = num
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.email = email
        self.senha = senha
        self.tipo = tipo

    def __str__(self):
        return f"[{self.id}] {self.nome} - {self.tipo}."
    
    def exibirMenu(self):
        print("0 - Logout")
        print("1 - Atualizar dados")
        print("2 - Apagar conta")
    
    @staticmethod
    def listarUsuarios(lista_usuarios):
        print("\nUsuários Cadastrados:")
        if not lista_usuarios:
            print("Nenhum usuário cadastrado.")
            return
        for u in lista_usuarios:
            print(u)

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
