from .Usuario import Usuario

class Atendente(Usuario):
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, turno):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Atendente")
        self.turno = turno
    
    def obter_funcionalidades(self):
        acoes = super().obter_funcionalidades() # Pega as ações de atualizar/excluir
        acoes.extend([
            ("🎧 Atendimentos Ativos", lambda container: self.gui_ref.tela_gerenciar_atendimentos(container)),
            ("⚠️ Gerenciar Alertas", lambda container: self.gui_ref.tela_painel_alertas(container))
        ])
        return acoes

    def analisarOcorrencia(self, ocorrencia):
        print(f"\nAnalisando ocorrência: {ocorrencia}")
        print("Vítimas envolvidas:")
        for vitima in ocorrencia.vitimas:
            print(f" - {vitima.nome}")
            print(f"   Idade: {vitima.idade}")
            print(f"   Situação: {vitima.situacao}")
