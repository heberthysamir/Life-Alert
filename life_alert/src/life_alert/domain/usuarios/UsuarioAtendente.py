from .Usuario import Usuario

class Atendente(Usuario):
    """
    Especiaização de Usuario para os operadores do centro de atendimento.
    Responsável por analisar ocorrências recebidas, gerenciar alertas e 
    encaminhar chamados para as equipes.
    """
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, turno):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Atendente")
        self._turno = turno

    def obter_funcionalidades(self):
        """Retorna as ações disponíveis para este usuário na interface."""
        acoes = super().obter_funcionalidades() # Pega as ações de atualizar/excluir
        acoes.extend([
            ("🎧 Atendimentos Ativos", lambda container: self.gui_ref.tela_gerenciar_atendimentos(container)),
            ("⚠️ Gerenciar Alertas", lambda container: self.gui_ref.tela_painel_alertas(container))
        ])
        return acoes
    
    def __str__(self):
        """Representação para exibição em logs."""
        id_display = self.id if self.id else "Novo"
        return f"[{id_display}] {self.nome} ({self.tipo})"

    def __repr__(self):
            """Representação técnica do Atendente."""
            return f"Atendente(nome='{self.nome}', turno='{self.turno}')"
