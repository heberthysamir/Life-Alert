from .Usuario import Usuario
from domain.Vitima import Vitima

class Agente(Usuario):
    def __init__(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, cargo, status):
        super().__init__(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha, tipo="Agente")
        self.cargo = cargo
        self.status = status
    
    def exibirMenu(self):
        super().exibirMenu()
        print("3 - Gerenciar Resgate em Andamento")
        print("4 - Cadastrar Vítima")
        if self.cargo.lower() == "lider":
            print("5 - Cadastrar Equipe")
            print("6 - Gerenciar Membros")

    def cadastrarVitima(self, lista_ocorrencias):
        print("\nCadastro de Vítima:\n")
        nome = input("Nome: ")
        idade = input("Idade: ")
        situacao = input("Situação: ")

        ocorrencia_id = input("ID da Ocorrência relacionada: ")
        ocorrencia = next((o for o in lista_ocorrencias if str(o.id) == ocorrencia_id), None)
        if not ocorrencia:
            print("Ocorrência não encontrada.")
            return None
        
        nova_vitima = Vitima(nome, idade, situacao, ocorrencia)
        ocorrencia.vitimas.append(nova_vitima)
        print(f"Vítima '{nome}' cadastrada na ocorrência ID {ocorrencia_id}.")

        return nova_vitima

    def atualizarOcorrencia():
        pass

    def cadastrarEquipe():
        pass

    def removerEquipe():
        pass
