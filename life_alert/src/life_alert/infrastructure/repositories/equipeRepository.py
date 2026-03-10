from infrastructure.database.connection import getDbConnection

class EquipeRepository:
    """Repository para gerenciar Equipes de Resgate com persistência garantida"""
    
    def salvar(self, equipe):
        """Salva equipe e garante o vínculo dos agentes no banco"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            if hasattr(equipe, 'id') and equipe.id:
                # UPDATE
                cursor.execute("""
                    UPDATE equipes_resgate
                    SET localidade=?, status=?, setor=?, especialidade=?
                    WHERE id=?
                """, (equipe.localidade, equipe.status, equipe.setor, equipe.especialidade, equipe.id))
            else:
                # INSERT
                cursor.execute("""
                    INSERT INTO equipes_resgate (localidade, status, setor, especialidade)
                    VALUES (?, ?, ?, ?)
                """, (equipe.localidade, equipe.status, equipe.setor, equipe.especialidade))
                equipe.id = cursor.lastrowid
                
                # --- O PONTO CRÍTICO: SALVAR OS AGENTES DA FACTORY ---
                if hasattr(equipe, 'agentes') and equipe.agentes:
                    for agente in equipe.agentes:
                        print(f"DEBUG REPO: Vinculando Agente ID {agente.id} à nova Equipe ID {equipe.id}")
                        cursor.execute("""
                            INSERT INTO equipe_agentes (equipe_id, agente_id)
                            VALUES (?, ?)
                        """, (equipe.id, agente.id))
            
            conn.commit()
            return equipe
    
    def listarTodos(self):
        """Retorna todas as equipes reconstruindo os objetos"""
        with getDbConnection() as conn:
            # Forçamos o row_factory para Row para facilitar o mapeamento
            import sqlite3
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipes_resgate")
            linhas = cursor.fetchall()
            
            # Passamos 'self' e 'linha'. A conexão nós tratamos dentro do instanciar
            return [self._instanciar_equipe(linha) for linha in linhas] if linhas else []
    
    def buscarPorId(self, id):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipes_resgate WHERE id = ?", (id,))
            linha = cursor.fetchone()
            return self._instanciar_equipe(linha) if linha else None

    def excluir(self, id):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            # Deleta os vínculos primeiro (chave estrangeira)
            cursor.execute("DELETE FROM equipe_agentes WHERE equipe_id = ?", (id,))
            cursor.execute("DELETE FROM equipes_resgate WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0

    def adicionarAgente(self, equipe_id, agente_id):
        """Adiciona agente à equipe no banco e comita"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO equipe_agentes (equipe_id, agente_id)
                    VALUES (?, ?)
                """, (equipe_id, agente_id))
                conn.commit()
                return True
            except:
                return False

    def removerAgente(self, equipe_id, agente_id):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM equipe_agentes 
                WHERE equipe_id = ? AND agente_id = ?
            """, (equipe_id, agente_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def buscarPorAgente(self, agente_id):
        with getDbConnection() as conn:
            cursor = conn.cursor()
            # Busca na tabela de vínculos (muitos-para-muitos)
            cursor.execute("SELECT equipe_id FROM equipe_agentes WHERE agente_id = ?", (agente_id,))
            linha = cursor.fetchone()
            if linha:
                return self.buscarPorId(linha[0])
            return None

    def _instanciar_equipe(self, linha):
        """Transforma linha do banco em objeto EquipeResgate com agentes"""
        if not linha: return None
        
        from domain.EquipeResgate import EquipeResgate
        from infrastructure.repositories.usuarioRepository import UsuarioRepository
        
        # Mapeamento seguro de dados
        eq_id = linha['id']
        
        # --- BUSCA DE AGENTES ---
        agentes_carregados = []
        user_repo = UsuarioRepository()
        
        # Abrimos uma conexão dedicada para os agentes para não dar conflito de Row
        with getDbConnection() as conn:
            conn.row_factory = None 
            cursor = conn.cursor()
            cursor.execute("SELECT agente_id FROM equipe_agentes WHERE equipe_id = ?", (eq_id,))
            vinc_ids = cursor.fetchall()
            
            for v in vinc_ids:
                ag_id = v[0]
                agente_obj = user_repo.buscarPorId(ag_id)
                
                if agente_obj:
                    agentes_carregados.append(agente_obj)
                else:
                    p = user_repo.criar_usuario_temporario(ag_id)
                    agentes_carregados.append(p)

        # Criamos o objeto final
        equipe = EquipeResgate(
            agentes=agentes_carregados,
            localidade=linha['localidade'],
            status=linha['status'],
            setor=linha['setor'],
            especialidade=linha['especialidade']
        )
        equipe.id = eq_id
        
        print(f"DEBUG REPO: Equipe {equipe.id} instanciada com {len(equipe.agentes)} agentes.")
        return equipe