from infrastructure.database.connection import getDbConnection
from domain.Alerta import Alerta

class AlertaRepository:
    """Repository para gerenciar Alertas no banco de dados"""
    
    def salvar(self, alerta):
        """Salva ou atualiza alerta no banco"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            # Garante que pegamos apenas o ID caso ocorrencia seja um objeto
            id_oc = getattr(alerta.ocorrencia, 'id', alerta.ocorrencia)

            if hasattr(alerta, 'id') and alerta.id:
                cursor.execute("""
                    UPDATE alertas
                    SET titulo=?, mensagem=?, ocorrencia_id=?, escopo=?, horario=?
                    WHERE id=?
                """, (alerta.titulo, alerta.mensagem, id_oc, alerta.escopo, alerta.horario, alerta.id))
            else:
                cursor.execute("""
                    INSERT INTO alertas (titulo, mensagem, ocorrencia_id, escopo, horario)
                    VALUES (?, ?, ?, ?, ?)
                """, (alerta.titulo, alerta.mensagem, id_oc, alerta.escopo, alerta.horario))
                alerta.id = cursor.lastrowid
            
            conn.commit() # Importante: garante a persistência física dos dados
            return alerta
    
    def listarTodos(self):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alertas")
            linhas = cursor.fetchall()
            print(f"DEBUG: Encontrados {len(linhas)} alertas no banco.")
            return [self._instanciar_alerta(linha) for linha in linhas]
    
    def excluir(self, id_alerta):
        """Remove um alerta do banco de dados pelo seu ID único"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            # Executa o DELETE baseado na chave primária
            cursor.execute("DELETE FROM alertas WHERE id = ?", (id_alerta,))
            conn.commit() # VITAL: sem o commit, a exclusão não é gravada no disco
            
            # Retorna True se pelo menos uma linha foi afetada (excluída)
            return cursor.rowcount > 0

    def _instanciar_alerta(self, linha):
        """Converte linha do banco em objeto Alerta com a Ocorrência completa"""
        if not linha:
            return None
        
        # 1. Buscamos a ocorrência completa pelo ID que está na coluna 'ocorrencia_id'
        from infrastructure.repositories.repositoryContainer import get_repositories
        repos = get_repositories()
        
        # Buscamos o objeto Ocorrencia real
        id_oc = linha['ocorrencia_id']
        objeto_ocorrencia = repos.ocorrencia.buscarPorId(id_oc)
        
        # 2. Criamos o Alerta passando o OBJETO e não apenas o ID
        alerta = Alerta(
            titulo=linha['titulo'],
            mensagem=linha['mensagem'],
            ocorrencia=objeto_ocorrencia, # Aqui agora vai o objeto completo
            escopo=linha['escopo'],
            horario=linha['horario']
        )
        alerta.id = linha['id']
        return alerta