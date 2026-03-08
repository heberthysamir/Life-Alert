from life_alert.infrastructure.repositories.usuarioRepository import UsuarioRepository
from life_alert.domain.usuarios.UsuarioCivil import Civil
from life_alert.domain.usuarios.UsuarioAtendente import Atendente
from life_alert.domain.usuarios.UsuarioAgente import Agente
import sqlite3

class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def realizar_login(self, email, senha):
        return self.repository.buscar_por_credenciais(email, senha)

    def cadastrar_civil(self, nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha):
        novo_civil = Civil(nome, cpf, telefone, rua, num, bairro, cidade, estado, email, senha)
        try:
            return self.repository.salvar(novo_civil)
        except sqlite3.IntegrityError:
            raise ValueError("Erro: CPF ou Email já cadastrados no sistema.")

    def listar_todos(self):
        return self.repository.buscar_todos()
        
    def atualizar_dados_usuario(self, usuario):
        return self.repository.salvar(usuario)

    def excluir_usuario(self, cpf):
        return self.repository.excluir(cpf)