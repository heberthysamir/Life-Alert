from life_alert.infrastructure.database.connection import getDbConnection
from life_alert.domain.ocorrencias.Ocorrencia import Ocorrencia
from life_alert.domain.ocorrencias.OcorrenciaMedica import OcorrenciaMedica
from life_alert.domain.ocorrencias.OcorrenciaPolicial import OcorrenciaPolicial
from datetime import datetime
import json


class OcorrenciaRepository:
    def salvar(self, ocorrencia):
        with getDbConnection() as conn:
            cursor = conn.cursor()

            tipo = "Medica" if isinstance(ocorrencia, OcorrenciaMedica) else ("Policial" if isinstance(ocorrencia, OcorrenciaPolicial) else "geral")
            
            perfil_medico = getattr(ocorrencia, 'perfilMedico', None) if isinstance(ocorrencia, OcorrenciaMedica) else None
            sintomas = getattr(ocorrencia, 'sintomas', None) if isinstance(ocorrencia, OcorrenciaMedica) else None
            prontuarios_vitimas = json.dumps(getattr(ocorrencia, 'prontuariosVitimas', {})) if isinstance(ocorrencia, OcorrenciaMedica) else None

            if hasattr(ocorrencia, 'id') and ocorrencia.id:
                cursor.execute("SELECT 1 FROM ocorrencias WHERE id = ?", (ocorrencia.id,))
                existe = cursor.fetchone()
            else:
                existe = None

            if existe:
                cursor.execute("""
                    UPDATE ocorrencias
                    SET atendente_id=?, agente_id=?, civil_id=?, equipe_id=?,
                        data_hora=?, status=?, descricao=?, rua=?, bairro=?,
                        cidade=?, estado=?, gravidade=?, tipo=?, qtd_afetados=?,
                        perfil_medico=?, sintomas=?, prontuarios_vitimas=?
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
                    perfil_medico,
                    sintomas,
                    prontuarios_vitimas,
                    ocorrencia.id
                ))
            else:
                # INSERT
                cursor.execute("""
                    INSERT INTO ocorrencias 
                    (atendente_id, agente_id, civil_id, equipe_id, data_hora,
                     status, descricao, rua, bairro, cidade, estado, gravidade, 
                     tipo, qtd_afetados, perfil_medico, sintomas, prontuarios_vitimas)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    perfil_medico,
                    sintomas,
                    prontuarios_vitimas
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
            'tipo': linha['tipo'],
            'qtdAfetados': linha['qtd_afetados']
        }
        
        if tipo == 'Medica':
            kwargs.update({
                'perfilMedico': linha['perfil_medico'],
                'sintomas': linha['sintomas'],
                'prontuariosVitimas': json.loads(linha['prontuarios_vitimas']) if linha['prontuarios_vitimas'] else {}
            })
            oc = OcorrenciaMedica(**kwargs)
        elif tipo == 'Policial':
            oc = OcorrenciaPolicial(tipoCrime='desconhecido', qtdCriminosos=0, descricaoSuspeito='desconhecido', **kwargs)
        else:
            oc = Ocorrencia(**kwargs)
        
        oc.id = linha['id']

        from .repositoryContainer import get_repositories
        repos = get_repositories()
        if linha['civil_id']:
            oc.civil = repos.usuario.buscarPorId(linha['civil_id'])
        if linha['atendente_id']:
            oc.atendente = repos.usuario.buscarPorId(linha['atendente_id'])
        if linha['agente_id']:
            oc.agente = repos.usuario.buscarPorId(linha['agente_id'])
        if linha['equipe_id']:
            oc.equipe = repos.equipe.buscarPorId(linha['equipe_id'])
        
        return oc
