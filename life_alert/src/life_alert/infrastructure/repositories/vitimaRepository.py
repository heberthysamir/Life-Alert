from life_alert.infrastructure.database.connection import getDbConnection
from life_alert.domain.Vitima import Vitima


class VitimaRepository:
    def salvar(self, vitima):
        """Salva vítima - sempre vinculada a uma ocorrência existente"""
        if not vitima.ocorrencia:
            raise ValueError("Vítima deve estar vinculada a uma ocorrência.")

        ocorrencia_id = getattr(vitima.ocorrencia, 'id', vitima.ocorrencia)
        if not ocorrencia_id:
            raise ValueError("A ocorrência deve ter ID válido.")

        with getDbConnection() as conn:
            cursor = conn.cursor()

            if hasattr(vitima, 'id') and vitima.id:
                cursor.execute("""
                    UPDATE vitimas
                    SET nome=?, idade=?, situacao=?
                    WHERE id=? AND ocorrencia_id=?
                """, (
                    vitima.nome,
                    vitima.idade,
                    vitima.situacao,
                    vitima.id,
                    ocorrencia_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO vitimas (nome, idade, situacao, ocorrencia_id)
                    VALUES (?, ?, ?, ?)
                """, (
                    vitima.nome,
                    vitima.idade,
                    vitima.situacao,
                    ocorrencia_id
                ))
                vitima.id = cursor.lastrowid

            return vitima

    def listarTodos(self):
        """Retorna todas as vítimas com suas ocorrências"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, o.descricao as ocorrencia_descricao
                FROM vitimas v
                JOIN ocorrencias o ON v.ocorrencia_id = o.id
            """)
            linhas = cursor.fetchall()
            return [self._instanciar_vitima(linha) for linha in linhas] if linhas else []

    def buscarPorId(self, id):
        """Busca vítima específica com sua ocorrência"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, o.descricao as ocorrencia_descricao
                FROM vitimas v
                JOIN ocorrencias o ON v.ocorrencia_id = o.id
                WHERE v.id = ?
            """, (id,))
            linha = cursor.fetchone()
            return self._instanciar_vitima(linha) if linha else None

    def buscarPorOcorrencia(self, ocorrencia_id):
        """Busca todas as vítimas de uma ocorrência específica"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, o.descricao as ocorrencia_descricao
                FROM vitimas v
                JOIN ocorrencias o ON v.ocorrencia_id = o.id
                WHERE v.ocorrencia_id = ?
            """, (ocorrencia_id,))
            linhas = cursor.fetchall()
            return [self._instanciar_vitima(linha) for linha in linhas] if linhas else []

    def buscarPorSituacao(self, situacao):
        """Busca vítimas por situação"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, o.descricao as ocorrencia_descricao
                FROM vitimas v
                JOIN ocorrencias o ON v.ocorrencia_id = o.id
                WHERE v.situacao = ?
            """, (situacao,))
            linhas = cursor.fetchall()
            return [self._instanciar_vitima(linha) for linha in linhas] if linhas else []

    def excluir(self, id):
        """Remove vítima específica"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vitimas WHERE id = ?", (id,))
            return cursor.rowcount > 0

    def excluirPorOcorrencia(self, ocorrencia_id):
        """Remove todas as vítimas de uma ocorrência"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vitimas WHERE ocorrencia_id = ?", (ocorrencia_id,))
            return cursor.rowcount

    def contarPorOcorrencia(self, ocorrencia_id):
        """Conta quantas vítimas existem em uma ocorrência"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM vitimas WHERE ocorrencia_id = ?", (ocorrencia_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0

    def _instanciar_vitima(self, linha):
        """Converte linha do banco em objeto Vitima com ocorrência"""
        if not linha:
            return None

        class OcorrenciaStub:
            def __init__(self, id, descricao):
                self.id = id
                self.descricao = descricao

        ocorrencia_stub = OcorrenciaStub(linha['ocorrencia_id'], linha.get('ocorrencia_descricao', ''))

        vitima = Vitima(
            nome=linha['nome'],
            idade=linha['idade'],
            situacao=linha['situacao'],
            ocorrencia=ocorrencia_stub
        )
        vitima.id = linha['id']
        return vitima
