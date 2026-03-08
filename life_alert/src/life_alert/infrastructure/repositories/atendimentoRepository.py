from ..database.connection import getDbConnection
from ...domain.Atendimento import Atendimento
from datetime import datetime


class AtendimentoRepository:
    """Repository para gerenciar Atendimentos no banco de dados"""
    
    def salvar(self, atendimento):
        """Salva ou atualiza atendimento"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            # Criar tabela de atendimentos se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS atendimentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    atendente_id INTEGER,
                    ocorrencia_id INTEGER,
                    civil_id INTEGER,
                    grau_urgencia TEXT,
                    relatorio TEXT,
                    hora_inicio TEXT,
                    hora_final TEXT,
                    FOREIGN KEY(atendente_id) REFERENCES usuarios(id),
                    FOREIGN KEY(ocorrencia_id) REFERENCES ocorrencias(id),
                    FOREIGN KEY(civil_id) REFERENCES usuarios(id)
                )
            """)
            
            if hasattr(atendimento, 'id') and atendimento.id:
                cursor.execute("""
                    UPDATE atendimentos
                    SET atendente_id=?, ocorrencia_id=?, civil_id=?, grau_urgencia=?,
                        relatorio=?, hora_inicio=?, hora_final=?
                    WHERE id=?
                """, (
                    getattr(atendimento.atendente, 'id', None) if atendimento.atendente else None,
                    getattr(atendimento.ocorrencia, 'id', None) if atendimento.ocorrencia else None,
                    getattr(atendimento.civil, 'id', None) if atendimento.civil else None,
                    atendimento.grauUrgencia,
                    atendimento.relatorio,
                    atendimento.horaInicio,
                    atendimento.horaFinal,
                    atendimento.id
                ))
            else:
                cursor.execute("""
                    INSERT INTO atendimentos 
                    (atendente_id, ocorrencia_id, civil_id, grau_urgencia, relatorio, hora_inicio, hora_final)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    getattr(atendimento.atendente, 'id', None) if atendimento.atendente else None,
                    getattr(atendimento.ocorrencia, 'id', None) if atendimento.ocorrencia else None,
                    getattr(atendimento.civil, 'id', None) if atendimento.civil else None,
                    atendimento.grauUrgencia,
                    atendimento.relatorio,
                    atendimento.horaInicio,
                    atendimento.horaFinal
                ))
                atendimento.id = cursor.lastrowid
            
            return atendimento
    
    def listarTodos(self):
        """Retorna todos os atendimentos"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM atendimentos")
                linhas = cursor.fetchall()
                return [self._instanciar_atendimento(linha) for linha in linhas] if linhas else []
            except:
                return []
    
    def buscarPorId(self, id):
        """Busca atendimento específico"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM atendimentos WHERE id = ?", (id,))
                linha = cursor.fetchone()
                return self._instanciar_atendimento(linha) if linha else None
            except:
                return None
    
    def buscarPorOcorrencia(self, ocorrencia_id):
        """Busca atendimentos de uma ocorrência"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM atendimentos WHERE ocorrencia_id = ?", (ocorrencia_id,))
                linhas = cursor.fetchall()
                return [self._instanciar_atendimento(linha) for linha in linhas] if linhas else []
            except:
                return []
    
    def excluir(self, id):
        """Remove atendimento"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM atendimentos WHERE id = ?", (id,))
                return cursor.rowcount > 0
            except:
                return False
    
    def _instanciar_atendimento(self, linha):
        """Converte linha do banco em objeto Atendimento"""
        if not linha:
            return None
        
        atendimento = Atendimento(
            atendente=None,
            ocorrencia=None,
            civil=None,
            grauUrgencia=linha['grau_urgencia'],
            relatorio=linha['relatorio'],
            horaInicio=linha['hora_inicio'],
            horaFinal=linha['hora_final']
        )
        atendimento.id = linha['id']
        return atendimento
