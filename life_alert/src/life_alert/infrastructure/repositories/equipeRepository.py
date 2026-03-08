from ..database.connection import getDbConnection


class EquipeRepository:
    """Repository para gerenciar Equipes de Resgate"""
    
    def salvar(self, equipe):
        """Salva ou atualiza equipe"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            if hasattr(equipe, 'id') and equipe.id:
                cursor.execute("""
                    UPDATE equipes_resgate
                    SET localidade=?, status=?, setor=?, especialidade=?
                    WHERE id=?
                """, (
                    equipe.localidade,
                    equipe.status,
                    equipe.setor,
                    equipe.especialidade,
                    equipe.id
                ))
            else:
                cursor.execute("""
                    INSERT INTO equipes_resgate (localidade, status, setor, especialidade)
                    VALUES (?, ?, ?, ?)
                """, (
                    equipe.localidade,
                    equipe.status,
                    equipe.setor,
                    equipe.especialidade
                ))
                equipe.id = cursor.lastrowid
                
                # Salvar agentes da equipe
                if hasattr(equipe, 'agentes') and equipe.agentes:
                    for agente in equipe.agentes:
                        cursor.execute("""
                            INSERT INTO equipe_agentes (equipe_id, agente_id)
                            VALUES (?, ?)
                        """, (equipe.id, agente.id))
            
            return equipe
    
    def listarTodos(self):
        """Retorna todas as equipes"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipes_resgate")
            linhas = cursor.fetchall()
            return [self._instanciar_equipe(linha) for linha in linhas] if linhas else []
    
    def buscarPorId(self, id):
        """Busca equipe específica"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipes_resgate WHERE id = ?", (id,))
            linha = cursor.fetchone()
            return self._instanciar_equipe(linha) if linha else None
    
    def buscarPorStatus(self, status):
        """Busca equipes por status"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipes_resgate WHERE status = ?", (status,))
            linhas = cursor.fetchall()
            return [self._instanciar_equipe(linha) for linha in linhas] if linhas else []
    
    def buscarPorLocalidade(self, localidade):
        """Busca equipes por localidade"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipes_resgate WHERE localidade = ?", (localidade,))
            linhas = cursor.fetchall()
            return [self._instanciar_equipe(linha) for linha in linhas] if linhas else []
    
    def excluir(self, id):
        """Remove equipe"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM equipe_agentes WHERE equipe_id = ?", (id,))
            cursor.execute("DELETE FROM equipes_resgate WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def adicionarAgente(self, equipe_id, agente_id):
        """Adiciona agente à equipe"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO equipe_agentes (equipe_id, agente_id)
                    VALUES (?, ?)
                """, (equipe_id, agente_id))
                return True
            except:
                return False
    
    def removerAgente(self, equipe_id, agente_id):
        """Remove agente da equipe"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM equipe_agentes 
                WHERE equipe_id = ? AND agente_id = ?
            """, (equipe_id, agente_id))
            return cursor.rowcount > 0
    
    def _instanciar_equipe(self, linha):
        """Converte linha do banco em objeto EquipeResgate"""
        if not linha:
            return None
        
        from ...domain.EquipeResgate import EquipeResgate
        
        equipe = EquipeResgate(
            agentes=[],
            localidade=linha['localidade'],
            status=linha['status'],
            setor=linha['setor'],
            especialidade=linha['especialidade']
        )
        equipe.id = linha['id']
        
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.* FROM usuarios u
                JOIN equipe_agentes ea ON u.id = ea.agente_id
                WHERE ea.equipe_id = ?
            """, (equipe.id,))
            agentes = cursor.fetchall()
        
        return equipe
