from life_alert.infrastructure.database.connection import getDbConnection
from life_alert.domain.Vitima import Vitima

class VitimaRepository:
<<<<<<< HEAD
    """Repository para gerenciar Vítimas vinculadas a uma Ocorrência (via Atendimento)"""

=======
>>>>>>> aad344b18f7c4b637ca42e7bff4b9b5c41c5c565
    def salvar(self, vitima):
        """Salva vítima - extrai o ID da ocorrência do objeto de resgate se necessário"""
        if not vitima.ocorrencia:
            raise ValueError("Vítima deve estar vinculada a uma ocorrência ou resgate.")

        if hasattr(vitima.ocorrencia, 'ocorrencia'):
            ocorrencia_id = vitima.ocorrencia.ocorrencia.id
        else:
            ocorrencia_id = getattr(vitima.ocorrencia, 'id', vitima.ocorrencia)

        if not ocorrencia_id:
            raise ValueError("Não foi possível determinar o ID da ocorrência para esta vítima.")

        with getDbConnection() as conn:
            conn.row_factory = lambda cursor, row: {col[0]: row[i] for i, col in enumerate(cursor.description)}
            cursor = conn.cursor()

            if hasattr(vitima, 'id') and vitima.id:
<<<<<<< HEAD
                # UPDATE
=======
>>>>>>> aad344b18f7c4b637ca42e7bff4b9b5c41c5c565
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
<<<<<<< HEAD
                # INSERT
=======
>>>>>>> aad344b18f7c4b637ca42e7bff4b9b5c41c5c565
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

            conn.commit()
            return vitima

    def listarTodos(self):
        """Retorna todas as vítimas do banco"""
        with getDbConnection() as conn:
            conn.row_factory = lambda cursor, row: {col[0]: row[i] for i, col in enumerate(cursor.description)}
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, o.tipo as ocorrencia_tipo, o.descricao as ocorrencia_desc
                FROM vitimas v
                JOIN ocorrencias o ON v.ocorrencia_id = o.id
            """)
            linhas = cursor.fetchall()
<<<<<<< HEAD
            return [self._instanciar_vitima(linha) for linha in linhas]
=======
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
>>>>>>> aad344b18f7c4b637ca42e7bff4b9b5c41c5c565

    def _instanciar_vitima(self, linha):
        if not linha: return None

<<<<<<< HEAD
        # Garante que a idade seja sempre um inteiro válido
        raw_idade = linha.get('idade')
        try:
            idade_limpa = int(raw_idade) if raw_idade is not None else 0
        except (ValueError, TypeError):
            idade_limpa = 0
=======
        class OcorrenciaStub:
            def __init__(self, id, descricao):
                self.id = id
                self.descricao = descricao
>>>>>>> aad344b18f7c4b637ca42e7bff4b9b5c41c5c565

        # Cria o vínculo para a interface encontrar o ID
        class ResgateStub:
            def __init__(self, id_oc):
                self.id = id_oc
                self.ocorrencia = self 

        vitima = Vitima(
            nome=linha['nome'],
            idade=idade_limpa,
            situacao=linha['situacao'],
            ocorrencia=ResgateStub(linha['ocorrencia_id'])
        )
        vitima.id = linha['id']
        return vitima