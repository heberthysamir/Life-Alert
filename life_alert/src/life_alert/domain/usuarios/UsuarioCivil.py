from .Usuario import Usuario

class Civil(Usuario):
    """
    Especialização de Usuario para o cidadão comum.
    É o ponto de entrada de novas ocorrências no sistema.
    """
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Civil")
        self.perfil_medico = None
    
    def obter_funcionalidades(self):
        """Retorna as ações disponíveis para este usuário na interface."""
        acoes = super().obter_funcionalidades() # Pega as ações de atualizar/excluir
        acoes.extend([
            ("🚨 Nova Ocorrência", lambda container: self.gui_ref.tela_criar_ocorrencia(container)),
            ("📋 Minhas Ocorrências", lambda container: self.gui_ref.tela_listar_ocorrencias(container)),
            ("🏥 Perfil Médico", lambda container: self.gui_ref.tela_perfil_medico(container))
        ])
        return acoes
    
    def __str__(self):
        """Representação para exibição em logs."""
        id_display = self.id if self.id else "Novo"
        return f"[{id_display}] {self.nome} ({self.tipo})"
    
    def __repr__(self):
        """Representação técnica do usuário Civil."""
        return f"Civil(nome='{self.nome}', cpf='{self.cpf}', email='{self.email}')"