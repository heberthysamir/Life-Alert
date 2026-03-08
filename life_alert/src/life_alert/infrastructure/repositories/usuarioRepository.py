from ..database.connection import getDbConnection
from ...domain.usuarios.UsuarioCivil import Civil
from ...domain.usuarios.UsuarioAtendente import Atendente
from ...domain.usuarios.UsuarioAgente import Agente

class UsuarioRepository:
    def salvar(self, usuario):
        with getDbConnection() as conn:
            cursor = conn.cursor()

            turno = getattr(usuario, 'turno', None)
            cargo = getattr(usuario, 'cargo', None)
            status = getattr(usuario, 'status', None)

            cursor.execute("SELECT id FROM usuarios WHERE cpf = ?", (usuario.cpf,))
            registro = cursor.fetchone()

            if registro:
                cursor.execute("""
                    UPDATE usuarios
                    SET nome=?, telefone=?, rua=?, num=?, bairro=?, cidade=?, estado=?, 
                        email=?, senha=?, turno=?, cargo=?, status=?
                    WHERE cpf=?
            """, (
                    usuario.nome, usuario.telefone, usuario.rua, usuario.num, 
                    usuario.bairro, usuario.cidade, usuario.estado, usuario.email, 
                    usuario.senha, turno, cargo, status, usuario.cpf
                ))
            else:
                cursor.execute("""
                    INSERT INTO usuarios (nome, cpf, telefone, rua, num, bairro, cidade, 
                                          estado, email, senha, tipo, turno, cargo, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    usuario.nome, usuario.cpf, usuario.telefone, usuario.rua, usuario.num, 
                    usuario.bairro, usuario.cidade, usuario.estado, usuario.email, 
                    usuario.senha, usuario.tipo, turno, cargo, status
                ))

                usuario.id = cursor.lastrowid
            
            return usuario

    def buscarPorCredenciais(self, email, senha):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            linha = cursor.fetchone()
            return self._instanciar_usuario(linha)
    
    def listarTodos(self):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            linhas = cursor.fetchall()    

            return [self._instanciar_usuario(linha) for linha in linhas]

    def buscarCpf(self, cpf):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
            linha = cursor.fetchone()
            return self._instanciar_usuario(linha)
    
    def excluir(self, cpf):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE cpf = ?", (cpf,))
            return cursor.rowcount > 0
    
    def _instanciar_usuario(self, linha):
        if not linha:
            return None
            
        tipo = linha['tipo']

        baseKwargs = {
            'nome': linha['nome'],
            'cpf': linha['cpf'],
            'telefone': linha['telefone'],
            'rua': linha['rua'],
            'num': linha['num'],
            'bairro': linha['bairro'],
            'cidade': linha['cidade'],
            'estado': linha['estado'],
            'email': linha['email'],
            'senha': linha['senha']
        }

        if tipo == 'Civil':
            usuario = Civil(**baseKwargs)
        elif tipo == 'Atendente':
            usuario = Atendente(**baseKwargs, turno=linha['turno'])
        elif tipo == 'Agente':
            usuario = Agente(**baseKwargs, cargo=linha['cargo'], status=linha['status'])
        else:
            raise ValueError(f"Tipo de usuário desconhecido no banco: {tipo}")
        
        usuario.id = linha['id']
        return usuario