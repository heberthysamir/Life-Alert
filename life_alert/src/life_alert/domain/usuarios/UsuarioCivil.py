from .Usuario import Usuario

class Civil(Usuario):
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Civil")
        self.perfil_medico = None
    
    def obter_funcionalidades(self):
        acoes = super().obter_funcionalidades() # Pega as ações de atualizar/excluir
        acoes.extend([
            ("🚨 Nova Ocorrência", lambda container: self.gui_ref.tela_criar_ocorrencia(container)),
            ("📋 Minhas Ocorrências", lambda container: self.gui_ref.tela_listar_ocorrencias(container)),
            ("🏥 Perfil Médico", lambda container: self.gui_ref.tela_perfil_medico(container))
        ])
        return acoes