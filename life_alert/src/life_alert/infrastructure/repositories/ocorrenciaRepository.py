from infrastructure.database.connection import getDbConnection
from domain.ocorrencias.Ocorrencia import Ocorrencia
from domain.ocorrencias.OcorrenciaMedica import OcorrenciaMedica
from domain.ocorrencias.OcorrenciaPolicial import OcorrenciaPolicial
from datetime import datetime


class OcorrenciaRepository:
    def salvar(self, ocorrencia):
        """Salva ou atualiza ocorrência no BD"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            if isinstance(ocorrencia, OcorrenciaMedica):
                tipo_persistido = "Medica"
            elif isinstance(ocorrencia, OcorrenciaPolicial):
                tipo_persistido = "Policial"
            else:
                tipo_persistido = "Generica"
            
            if hasattr(ocorrencia, 'id') and ocorrencia.id: 
                # UPDATE
                cursor.execute("""
                    UPDATE ocorrencias
                    SET atendente_id=?, agente_id=?, civil_id=?, equipe_id=?,
                        data_hora=?, status=?, descricao=?, rua=?, bairro=?,
                        cidade=?, estado=?, gravidade=?, tipo=?, qtd_afetados=?
                    WHERE id=?
                """, (
                    getattr(ocorrencia.atendente, 'id', None) if ocorrencia.atendente else None,
                    getattr(ocorrencia.agente, 'id', None) if ocorrencia.agente else None,
                    getattr(ocorrencia.civil, 'id', None) if ocorrencia.civil else None,
                    getattr(ocorrencia.equipe, 'id', None) if ocorrencia.equipe else None,
                    ocorrencia.dataHora,
                    ocorrencia.status,
                    ocorrencia.descricao,
                    ocorrencia.rua,
                    ocorrencia.bairro,
                    ocorrencia.cidade,
                    ocorrencia.estado,
                    ocorrencia.gravidade,
                    tipo_persistido,
                    ocorrencia.qtdAfetados,
                    ocorrencia.id
                ))
            else:
                # INSERT
                cursor.execute("""
                    INSERT INTO ocorrencias 
                    (atendente_id, agente_id, civil_id, equipe_id, data_hora,
                     status, descricao, rua, bairro, cidade, estado, gravidade, 
                     tipo, qtd_afetados)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    getattr(ocorrencia.atendente, 'id', None) if ocorrencia.atendente else None,
                    getattr(ocorrencia.agente, 'id', None) if ocorrencia.agente else None,
                    getattr(ocorrencia.civil, 'id', None) if ocorrencia.civil else None,
                    getattr(ocorrencia.equipe, 'id', None) if ocorrencia.equipe else None,
                    ocorrencia.dataHora,
                    ocorrencia.status,
                    ocorrencia.descricao,
                    ocorrencia.rua,
                    ocorrencia.bairro,
                    ocorrencia.cidade,
                    ocorrencia.estado,
                    ocorrencia.gravidade,
                    tipo_persistido,
                    ocorrencia.qtdAfetados
                ))
                ocorrencia.id = cursor.lastrowid
            
            return ocorrencia

    def listarTodos(self):
        """Retorna todas as ocorrências"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ocorrencias")
            linhas = cursor.fetchall()
            return [self._instanciar_ocorrencia(linha) for linha in linhas] if linhas else []
    
    def buscarPorCivil(self, civil_id):
        """Traz apenas as ocorrências do civil logado"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ocorrencias WHERE civil_id = ?", (civil_id,))
            linhas = cursor.fetchall()
            return [self._instanciar_ocorrencia(linha) for linha in linhas]

    def buscarPorAtendente(self, atendente_id):
        """Traz as ocorrências designadas para o atendente logado"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ocorrencias WHERE atendente_id = ?", (atendente_id,))
            linhas = cursor.fetchall()
            return [self._instanciar_ocorrencia(linha) for linha in linhas]

    def buscarPorId(self, id):
        """Busca ocorrência específica"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ocorrencias WHERE id = ?", (id,))
            linha = cursor.fetchone()
            return self._instanciar_ocorrencia(linha) if linha else None

    def buscarPorStatus(self, status):
        """Busca ocorrências por status"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ocorrencias WHERE status = ?", (status,))
            linhas = cursor.fetchall()
            return [self._instanciar_ocorrencia(linha) for linha in linhas] if linhas else []

    def excluir(self, id):
        """Deleta ocorrência"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ocorrencias WHERE id = ?", (id,))
            return cursor.rowcount > 0

    def _instanciar_ocorrencia(self, linha):
        if not linha:
            return None

        from .usuarioRepository import UsuarioRepository
        from .equipeRepository import EquipeRepository
        user_repo = UsuarioRepository()
        eq_repo = EquipeRepository()
        
        civil_obj = user_repo.buscarPorId(linha['civil_id']) if linha['civil_id'] else None
        atendente_obj = user_repo.buscarPorId(linha['atendente_id']) if linha['atendente_id'] else None
        agente_obj = user_repo.buscarPorId(linha['agente_id']) if linha['agente_id'] else None
        equipe_obj = eq_repo.buscarPorId(linha['equipe_id']) if linha['equipe_id'] else None


        tipo_banco = linha['tipo']
        
        kwargs = {
            'atendente': atendente_obj, 
            'agente': agente_obj,       
            'civil': civil_obj,         
            'dataHora': linha['data_hora'],
            'status': linha['status'],
            'descricao': linha['descricao'],
            'rua': linha['rua'],
            'bairro': linha['bairro'],
            'cidade': linha['cidade'],
            'estado': linha['estado'],
            'gravidade': linha['gravidade'],
            'qtdAfetados': linha['qtd_afetados'],
            'tipo': tipo_banco # Mantém o nome original (Ex: "Incêndio")
        }
        
        # DECISÃO DE INSTÂNCIA
        if tipo_banco == 'Medica':
            oc = OcorrenciaMedica(**kwargs)
        elif tipo_banco == 'Policial':
            # Preenche campos obrigatórios da subclasse policial
            kwargs['tipoCrime'] = getattr(linha, 'tipo_crime', "Não informado")
            kwargs['qtdCriminosos'] = getattr(linha, 'qtd_criminosos', 0)
            kwargs['descricaoSuspeito'] = getattr(linha, 'desc_suspeito', "Não informada")
            oc = OcorrenciaPolicial(**kwargs)
        else:
            # Se for 'Generica' ou qualquer outro tipo (Incêndio, Enchente, etc)
            # Instancia a superclasse Ocorrencia diretamente
            oc = Ocorrencia(**kwargs)
        
        oc.id = linha['id']
        oc.equipe = equipe_obj
        return oc
        