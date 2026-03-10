from life_alert.infrastructure.database.connection import getDbConnection
from life_alert.domain.Resgate import Resgate


class ResgateRepository:
    """Repository para gerenciar Resgates"""
    
    def salvar(self, resgate):
        """Salva ou atualiza resgate"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resgates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ocorrencia_id INTEGER,
                    data_inicio TEXT,
                    descricao TEXT,
                    data_fim TEXT,
                    qtd_resgatados INTEGER,
                    FOREIGN KEY(ocorrencia_id) REFERENCES ocorrencias(id)
                )
            """)
            
            exists = False
            if hasattr(resgate, 'id') and resgate.id:
                cursor.execute("SELECT 1 FROM resgates WHERE id = ?", (resgate.id,))
                exists = cursor.fetchone() is not None

            if exists:
                cursor.execute("""
                    UPDATE resgates
                    SET ocorrencia_id=?, data_inicio=?, descricao=?, data_fim=?, qtd_resgatados=?
                    WHERE id=?
                """, (
                    getattr(resgate.ocorrencia, 'id', resgate.ocorrencia) if hasattr(resgate, 'ocorrencia') else None,
                    resgate.dataInicio,
                    resgate.descricao,
                    resgate.dataFim,
                    resgate.qtdResgatados,
                    resgate.id
                ))
            else:
                cursor.execute("""
                    INSERT INTO resgates (ocorrencia_id, data_inicio, descricao, data_fim, qtd_resgatados)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    getattr(resgate.ocorrencia, 'id', resgate.ocorrencia) if hasattr(resgate, 'ocorrencia') else None,
                    resgate.dataInicio,
                    resgate.descricao,
                    resgate.dataFim,
                    resgate.qtdResgatados
                ))
                resgate.id = cursor.lastrowid
            
            return resgate
    
    def listarTodos(self):
        """Retorna todos os resgates"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM resgates")
                linhas = cursor.fetchall()
                return [self._instanciar_resgate(linha) for linha in linhas] if linhas else []
            except:
                return []
    
    def buscarPorId(self, id):
        """Busca resgate específico"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM resgates WHERE id = ?", (id,))
                linha = cursor.fetchone()
                return self._instanciar_resgate(linha) if linha else None
            except:
                return None
    
    def buscarPorOcorrencia(self, ocorrencia_id):
        """Busca resgates de uma ocorrência"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM resgates WHERE ocorrencia_id = ?", (ocorrencia_id,))
                linhas = cursor.fetchall()
                return [self._instanciar_resgate(linha) for linha in linhas] if linhas else []
            except:
                return []
    
    def excluir(self, id):
        """Remove resgate"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM resgates WHERE id = ?", (id,))
                return cursor.rowcount > 0
            except:
                return False
    
    def _instanciar_resgate(self, linha):
        """Converte linha do banco em objeto Resgate"""
        if not linha:
            return None
        
        resgate = Resgate(
            ocorrencia=linha['ocorrencia_id'],
            dataInicio=linha['data_inicio'],
            descricao=linha['descricao'],
            dataFim=linha['data_fim'],
            qtdResgatados=linha['qtd_resgatados']
        )
        resgate.id = linha['id']
        return resgate
