from .Usuario import Usuario
from domain.Vitima import Vitima

class Agente(Usuario):
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, cargo, status):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Agente")
        self.cargo = cargo
        self.status = status
    
    def obter_funcionalidades(self):
        acoes = super().obter_funcionalidades() # Pega as ações de atualizar/excluir
        acoes.extend([
            ("👥 Gerenciar Vítimas", lambda container: self.gui_ref.tela_gerenciar_vitimas(container)),
            ("🚩 Registrar Vítima", lambda container: self.gui_ref.tela_cadastrar_vitima(container))
        ])
        
        # Polimorfismo baseado no cargo
        if hasattr(self, 'cargo') and self.cargo.lower() == "lider":
            acoes.append(("🛠️ Criar Equipe", lambda container: self.gui_ref.tela_criar_equipe(container)))
            acoes.append(("📋 Menu Equipes", lambda container: self.gui_ref.tela_menu_equipe(container)))
            acoes.append(("📊 Relatórios", lambda container: self.gui_ref.tela_relatorios(container)))
            
        return acoes
    
    def atualizarOcorrencia():
        pass

    def cadastrarEquipe():
        pass

    def removerEquipe():
        pass
