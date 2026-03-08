from .connection import getDbConnection

def create_tables():
    with getDbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT,
                rua TEXT,
                num TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                turno TEXT, 
                cargo TEXT,
                status TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS perfis_medicos (
                usuario_id INTEGER PRIMARY KEY,
                alergias TEXT,
                doencas TEXT,
                deficiencia TEXT,
                tipo_sanguineo TEXT,
                contato_emerg TEXT,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipes_resgate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                localidade TEXT,
                status TEXT,
                setor TEXT,
                especialidade TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipe_agentes (
                equipe_id INTEGER,
                agente_id INTEGER,
                PRIMARY KEY (equipe_id, agente_id),
                FOREIGN KEY(equipe_id) REFERENCES equipes_resgate(id) ON DELETE CASCADE,
                FOREIGN KEY(agente_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                atendente_id INTEGER,
                agente_id INTEGER,
                civil_id INTEGER,
                equipe_id INTEGER,
                data_hora TEXT,
                status TEXT NOT NULL,
                descricao TEXT,
                rua TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                gravidade TEXT,
                tipo TEXT,
                qtd_afetados INTEGER,
                FOREIGN KEY(atendente_id) REFERENCES usuarios(id),
                FOREIGN KEY(agente_id) REFERENCES usuarios(id),
                FOREIGN KEY(civil_id) REFERENCES usuarios(id),
                FOREIGN KEY(equipe_id) REFERENCES equipes_resgate(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                ocorrencia_id INTEGER NOT NULL,
                escopo TEXT,
                horario TEXT,
                FOREIGN KEY(ocorrencia_id) REFERENCES ocorrencias(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vitimas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                situacao TEXT NOT NULL,
                ocorrencia_id INTEGER NOT NULL,
                FOREIGN KEY(ocorrencia_id) REFERENCES ocorrencias(id) ON DELETE CASCADE
            )
        """)