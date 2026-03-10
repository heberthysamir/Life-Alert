from infrastructure.database.connection import getDbConnection
from domain.Vitima import Vitima

class VitimaRepository:
    """Repository para gerenciar Vítimas vinculadas a uma Ocorrência (via Atendimento)"""

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
                # UPDATE
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
                # INSERT
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
            return [self._instanciar_vitima(linha) for linha in linhas]

    def _instanciar_vitima(self, linha):
        if not linha: return None

        # Garante que a idade seja sempre um inteiro válido
        raw_idade = linha.get('idade')
        try:
            idade_limpa = int(raw_idade) if raw_idade is not None else 0
        except (ValueError, TypeError):
            idade_limpa = 0

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