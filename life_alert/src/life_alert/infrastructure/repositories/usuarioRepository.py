from life_alert.infrastructure.database.connection import getDbConnection
from life_alert.domain.usuarios.UsuarioCivil import Civil
from life_alert.domain.usuarios.UsuarioAtendente import Atendente
from life_alert.domain.usuarios.UsuarioAgente import Agente

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
                    usuario._senha, turno, cargo, status, usuario.cpf
                ))
            else:
                cursor.execute("""
                    INSERT INTO usuarios (nome, cpf, telefone, rua, num, bairro, cidade, 
                                          estado, email, senha, tipo, turno, cargo, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    usuario.nome, usuario.cpf, usuario.telefone, usuario.rua, usuario.num, 
                    usuario.bairro, usuario.cidade, usuario.estado, usuario.email, 
                    usuario._senha, usuario.tipo, turno, cargo, status
                ))

                usuario.id = cursor.lastrowid
            
            return usuario

    def buscarPorCredenciais(self, email, _senha):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, _senha))
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
    
    def buscarPorId(self, id):
<<<<<<< HEAD
=======
        """Retorna um usuário dado seu id (ou None se não existir)."""
>>>>>>> aad344b18f7c4b637ca42e7bff4b9b5c41c5c565
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
            linha = cursor.fetchone()
<<<<<<< HEAD
            return self._instanciar_usuario(linha)
    
=======
            return self._instanciar_usuario(linha) if linha else None

>>>>>>> aad344b18f7c4b637ca42e7bff4b9b5c41c5c565
    def excluir(self, cpf):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE cpf = ?", (cpf,))
            return cursor.rowcount > 0
    
    def criar_usuario_temporario(self, id_agente):
        from domain.usuarios.UsuarioAgente import Agente
        # Preenchendo todos os 8 argumentos que o Python reclamou que faltavam
        u = Agente(
            nome=f"Agente {id_agente}", 
            cpf="000.000.000-00", 
            senha="senha123", # <--- Senha com mais de 6 caracteres
            cidade="Não informada",
            telefone="000000000",
            rua="Rua",
            num="0",
            bairro="Bairro",
            estado="ST",
            email=f"agente{id_agente}@lifealert.com", 
            cargo="Agente",
            status="Ativo"
        )
        u.id = id_agente
        return u
    
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