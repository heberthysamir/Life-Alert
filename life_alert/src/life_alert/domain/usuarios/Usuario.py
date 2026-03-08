class Usuario:
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo):
        self.id = None
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
        id_str = self.id if self.id else "Novo"
        return f"[{id_str}] {self.nome} - {self.tipo}."  
      
    def obter_funcionalidades(self):
        return [
            ("🔔 Ver Alertas", lambda container: self.gui_ref.tela_central_alertas(container)),
            ("👤 Atualizar Dados", lambda container: self.gui_ref.tela_atualizar_dados(container)),
            ("🗑️ Excluir Conta", lambda container: self.gui_ref.tela_excluir_conta(container))
        ]

    
    def atualizarUsuario(self, novo_nome=None, novo_telefone=None, novo_email=None, nova_senha=None, nova_rua=None, novo_num=None, novo_bairro=None, nova_cidade=None, novo_estado=None):
        if novo_nome: self.nome = novo_nome
        if novo_telefone: self.telefone = novo_telefone
        if novo_email: self.email = novo_email
        if nova_senha: self.senha = nova_senha

        if nova_rua: self.rua = nova_rua
        if novo_num: self.num = novo_num
        if novo_bairro: self.bairro = novo_bairro
        if nova_cidade: self.cidade = nova_cidade
        if novo_estado: self.estado = novo_estado
