from ..database.connection import getDbConnection
from ...domain.Alerta import Alerta


class AlertaRepository:
    """Repository para gerenciar Alertas no banco de dados"""
    
    def salvar(self, alerta):
        """Salva ou atualiza alerta no banco"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            if hasattr(alerta, 'id') and alerta.id:
                # UPDATE
                cursor.execute("""
                    UPDATE alertas
                    SET titulo=?, mensagem=?, ocorrencia_id=?, escopo=?, horario=?
                    WHERE id=?
                """, (
                    alerta.titulo,
                    alerta.mensagem,
                    getattr(alerta.ocorrencia, 'id', alerta.ocorrencia) if hasattr(alerta, 'ocorrencia') else None,
                    alerta.escopo,
                    alerta.horario,
                    alerta.id
                ))
            else:
                # INSERT
                cursor.execute("""
                    INSERT INTO alertas (titulo, mensagem, ocorrencia_id, escopo, horario)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    alerta.titulo,
                    alerta.mensagem,
                    getattr(alerta.ocorrencia, 'id', alerta.ocorrencia) if hasattr(alerta, 'ocorrencia') else None,
                    alerta.escopo,
                    alerta.horario
                ))
                alerta.id = cursor.lastrowid
            
            return alerta
    
    def listarTodos(self):
        """Retorna todos os alertas"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alertas")
            linhas = cursor.fetchall()
            return [self._instanciar_alerta(linha) for linha in linhas] if linhas else []
    
    def listarPorOcorrencia(self, ocorrencia_id):
        """Retorna alertas de uma ocorrência específica"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM alertas WHERE ocorrencia_id = ?",
                (ocorrencia_id,)
            )
            linhas = cursor.fetchall()
            return [self._instanciar_alerta(linha) for linha in linhas] if linhas else []
    
    def listarPorEscopo(self, escopo):
        """Filtra alertas por escopo"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM alertas WHERE escopo = ?",
                (escopo,)
            )
            linhas = cursor.fetchall()
            return [self._instanciar_alerta(linha) for linha in linhas] if linhas else []
    
    def buscarPorId(self, id):
        """Busca alerta específico"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alertas WHERE id = ?", (id,))
            linha = cursor.fetchone()
            return self._instanciar_alerta(linha) if linha else None
    
    def excluir(self, id):
        """Remove alerta por ID"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alertas WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def _instanciar_alerta(self, linha):
        """Converte linha do banco em objeto Alerta"""
        if not linha:
            return None
        
        alerta = Alerta(
            titulo=linha['titulo'],
            mensagem=linha['mensagem'],
            ocorrencia=linha['ocorrencia_id'],
            escopo=linha['escopo'],
            horario=linha['horario']
        )
        alerta.id = linha['id']
        return alerta
