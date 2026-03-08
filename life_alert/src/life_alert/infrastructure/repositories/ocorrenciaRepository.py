from ..database.connection import getDbConnection
from ...domain.ocorrencias.Ocorrencia import Ocorrencia
from ...domain.ocorrencias.OcorrenciaMedica import OcorrenciaMedica
from ...domain.ocorrencias.OcorrenciaPolicial import OcorrenciaPolicial
from datetime import datetime


class OcorrenciaRepository:
    def salvar(self, ocorrencia):
        """Salva ou atualiza ocorrência no BD"""
        with getDbConnection() as conn:
            cursor = conn.cursor()
            
            tipo = "Medica" if isinstance(ocorrencia, OcorrenciaMedica) else "Policial"
            
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
                    tipo,
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
                    tipo,
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
        
        tipo = linha['tipo']
        kwargs = {
            'atendente': None,
            'agente': None,
            'civil': None,
            'dataHora': linha['data_hora'],
            'status': linha['status'],
            'descricao': linha['descricao'],
            'rua': linha['rua'],
            'bairro': linha['bairro'],
            'cidade': linha['cidade'],
            'estado': linha['estado'],
            'gravidade': linha['gravidade'],
            'qtdAfetados': linha['qtd_afetados']
        }
        
        if tipo == 'Medica':
            oc = OcorrenciaMedica(**kwargs)
        else:
            oc = OcorrenciaPolicial(**kwargs)
        
        oc.id = linha['id']
        return oc
