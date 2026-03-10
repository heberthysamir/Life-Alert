from .Usuario import Usuario

class Agente(Usuario):
    """
    Especialização de Usuario para membros operacionais (Bombeiros, SAMU, etc).
    Possui permissões estendidas dependendo do cargo 
    """
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, cargo, status):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Agente")
        self.cargo = cargo
        self.status = status
    
    def obter_funcionalidades(self):
        """Retorna as ações disponíveis para este usuário na interface."""
        acoes = super().obter_funcionalidades() # Pega as ações de atualizar/excluir
        acoes.extend([ # Ações comuns a todos os agentes
            ("👥 Gerenciar Vítimas", lambda container: self.gui_ref.tela_gerenciar_vitimas(container)),
            ("Minhas Equipes & Resgates", lambda container: self.gui_ref.tela_painel_operacional(container)) 
        ])
        if hasattr(self, 'cargo') and self.cargo.lower() == "lider":
            acoes.append(("📋 Menu Equipes", lambda container: self.gui_ref.tela_menu_equipe(container)))
            acoes.append(("📊 Relatórios", lambda container: self.gui_ref.tela_relatorios(container)))
            
        return acoes
    
    def __str__(self):
        """Representação para exibição em logs."""
        id_display = self.id if self.id else "Novo"
        return f"[{id_display}] {self.nome} ({self.tipo})"
    
    def __repr__(self):
        """Representação técnica do Agente."""
        return f"Agente(nome='{self.nome}', cargo='{self.cargo}', status='{self.status}')"
