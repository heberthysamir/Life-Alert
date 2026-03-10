import pytest
from life_alert.domain.PerfilMedico import PerfilMedico
from life_alert.domain.Atendimento import Atendimento
from life_alert.domain.Alerta import Alerta
from life_alert.domain.Resgate import Resgate
from life_alert.domain.EquipeResgate import EquipeResgate
from life_alert.domain.Vitima import Vitima
from life_alert.application.atendimentoService import AtendimentoService

class MockUsuario:
    def __init__(self, id, nome, tipo, cidade):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.cidade = cidade
        self.status = "Disponível"

class MockOcorrencia:
    def __init__(self, id, cidade):
        self.id = id
        self.cidade = cidade
        self.status = "Aberta"
        self.vitimas = []

@pytest.fixture
def ocorrencia_padrao():
    return MockOcorrencia(id=1, cidade="Araripe")

@pytest.fixture
def agente_padrao():
    return MockUsuario(id=1, nome="Agente Silva", tipo="Agente", cidade="Caririaçu")

@pytest.fixture
def equipe_padrao(agente_padrao):
    equipe = EquipeResgate(agentes=[], localidade="Base 1", status="Disponível", setor="SAMU", especialidade="Médica")
    equipe.adicionar_membro(agente_padrao)
    return equipe

def test_resgate_inicializacao_data_padrao(ocorrencia_padrao):
    """Verifica se o Resgate gera automaticamente a dataInicio quando não fornecida"""
    resgate = Resgate(ocorrencia=ocorrencia_padrao, descricao="Busca inicial")
    
    assert resgate.dataInicio is not None
    assert "-" in resgate.dataInicio
    assert resgate.qtdResgatados == 0

def test_atendimento_inicializacao_horas_padrao(agente_padrao, ocorrencia_padrao):
    """Verifica se o Atendimento gera a horaInicio e deixa horaFinal vazia na criação"""
    atendimento = Atendimento(atendente=agente_padrao, ocorrencia=ocorrencia_padrao, civil="Maria")
    
    assert atendimento.horaInicio is not None
    assert atendimento.horaFinal is None

def test_resgate_qtd_resgatados_invalida_deve_falhar(ocorrencia_padrao):
    resgate = Resgate(ocorrencia=ocorrencia_padrao, dataInicio="2026-03-07")
    
    with pytest.raises(ValueError) as erro_negativo:
        resgate.qtdResgatados = -3
    assert "não pode ser negativa" in str(erro_negativo.value)
    
    with pytest.raises(ValueError) as erro_texto:
        resgate.qtdResgatados = "cinco"
    assert "número inteiro válido" in str(erro_texto.value)

def test_equipe_adicionar_membro_duplicado_deve_falhar(equipe_padrao, agente_padrao):
    with pytest.raises(ValueError) as erro:
        equipe_padrao.adicionar_membro(agente_padrao)
    
    assert "já está nesta equipe" in str(erro.value)

def test_equipe_remover_membro_com_sucesso(equipe_padrao, agente_padrao):
    equipe_padrao.remover_membro(agente_padrao.id)
    
    assert agente_padrao not in equipe_padrao.agentes
    assert len(equipe_padrao.agentes) == 0

def test_equipe_alterar_status_agente(equipe_padrao, agente_padrao):
    equipe_padrao.alterar_status_agente(agente_padrao.id, "Em Resgate")
    
    assert agente_padrao.status == "Em Resgate"

def test_designar_atendente_mesma_cidade_menor_fila():
    oc_rio = MockOcorrencia(id=2, cidade="Maurity")
    
    at_sp = MockUsuario(id=2, nome="Paulo", tipo="Atendente", cidade="Maurity")
    at_rio_ocupado = MockUsuario(id=3, nome="Ana", tipo="Atendente", cidade="Maurity")
    at_rio_livre = MockUsuario(id=4, nome="Carlos", tipo="Atendente", cidade="Maurity")
    
    lista_usuarios = [at_sp, at_rio_ocupado, at_rio_livre]
    
    class MockAtendimento:
        def __init__(self, atendente):
            self.atendente = atendente
            
    lista_atendimentos = [MockAtendimento(at_rio_ocupado), MockAtendimento(at_rio_ocupado)]

    atendente_designado = AtendimentoService.designarAtendente(oc_rio, lista_usuarios, lista_atendimentos)

    assert atendente_designado.nome == "Paulo"
    assert atendente_designado.cidade == "Maurity"

def test_atualizar_situacao_vitima_valida(ocorrencia_padrao):
    vitima = Vitima("João", "25", "Grave", ocorrencia_padrao)
    
    sucesso = vitima.atualizar_situacao("Estável")
    
    assert sucesso is True
    assert vitima.situacao == "Estável"

def test_atualizar_situacao_vitima_invalida_vazia(ocorrencia_padrao):
    vitima = Vitima("João", "25", "Grave", ocorrencia_padrao)
    
    sucesso = vitima.atualizar_situacao("   ")
    
    assert sucesso is False
    assert vitima.situacao == "Grave"

def test_perfil_medico_atualizar_dados_parcial():
    pm = PerfilMedico(alergias="Nenhuma", doencas="Asma", deficiencia="Nenhuma", tipoSanguineo="O+", contatoEmerg="1199999999")
    
    pm.atualizar_dados(nova_alergia="Amendoim")
    assert pm.alergias == "Amendoim"
    assert pm.doencas == "Asma"
    assert pm.tipoSanguineo == "O+"

def test_perfil_medico_str_format():
    pm = PerfilMedico("Pó", "Diabetes", "Visual", "A+", "123456")
    
    texto = str(pm)
    assert "Alergias: Pó" in texto
    assert "Doenças Crônicas: Diabetes" in texto
    assert "Deficiência: Visual" in texto

def test_equipe_remover_membro_inexistente_deve_falhar(equipe_padrao):
    with pytest.raises(ValueError) as erro:
        equipe_padrao.remover_membro(999)
    
    assert "Agente não encontrado" in str(erro.value)

def test_equipe_alterar_status_agente_inexistente_deve_falhar(equipe_padrao):
    with pytest.raises(ValueError) as erro:
        equipe_padrao.alterar_status_agente(999, "Em Resgate")
        
    assert "Agente não encontrado" in str(erro.value)

def test_atendimento_finalizar_adiciona_na_lista(agente_padrao, ocorrencia_padrao):
    lista_concluidos = []
    atendimento = Atendimento(atendente=agente_padrao, ocorrencia=ocorrencia_padrao, civil="Maria", grauUrgencia="Alta")
    
    atendimento.finalizarAtendimento(lista_concluidos)
    
    assert len(lista_concluidos) == 1
    assert lista_concluidos[0] == atendimento
    assert atendimento.horaFinal is not None

def test_resgate_adicionar_vitima(ocorrencia_padrao):
    resgate = Resgate(ocorrencia=ocorrencia_padrao, dataInicio="2026-03-07", descricao="Busca e Salvamento", dataFim=None, qtdResgatados=0)
    
    mensagem = resgate.adicionarVitima(5)
    
    assert resgate.qtdResgatados == 5
    assert "5" in mensagem

def test_alerta_str_format(ocorrencia_padrao):
    ocorrencia_padrao.bairro = "Malvinas"
    ocorrencia_padrao.cidade = "Barbalha"
    alerta = Alerta(titulo="Forte Chuva", mensagem="Evite sair de casa.", ocorrencia=ocorrencia_padrao, escopo="bairro", horario="15:00")
    
    texto = str(alerta)
    
    assert "Forte Chuva (15:00)" in texto
    assert "Local: Malvinas - Barbalha" in texto
    assert "Aviso: Evite sair de casa" in texto


def test_civil_registra_e_recupera_ocorrencia():
    """Garanta que uma ocorrência criada por um civil é persistida no banco
    e pode ser consultada posteriormente."""
    from life_alert.infrastructure.database.setup import create_tables
    from life_alert.infrastructure.repositories.usuarioRepository import UsuarioRepository
    from life_alert.infrastructure.repositories.ocorrenciaRepository import OcorrenciaRepository
    from life_alert.application.ocorrenciaFactory import OcorrenciaFactory
    from domain.usuarios.UsuarioCivil import Civil
    from datetime import datetime

    # garantir estrutura de banco existente
    create_tables()

    usuario_repo = UsuarioRepository()
    ocorr_repo = OcorrenciaRepository()

    # prepara usuário de teste (exclui se já existir e cria um novo)
    cpf_teste = "11122233344"
    antigo = usuario_repo.buscarCpf(cpf_teste)
    if antigo:
        usuario_repo.excluir(cpf_teste)
    civil = Civil(nome="Teste Civil", cpf=cpf_teste, telefone="0000", rua="R", num="1",
                  bairro="B", cidade="C", estado="E", email="civil@teste.com", senha="senha123")
    usuario_repo.salvar(civil)

    # cria ocorrência associada ao civil e salva
    oc = OcorrenciaFactory.criar("2",
                                 atendente=None, agente=None, civil=civil,
                                 dataHora=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 status="Aberta", descricao="Ocorrência de teste",
                                 rua="Alguma", bairro="Algum", cidade="Cidade",
                                 estado="EST", gravidade="Baixa", tipo="Médica", qtdAfetados=0)
    ocorr_repo.salvar(oc)

    todas = ocorr_repo.listarTodos()
    minhas = [o for o in todas if o.civil and getattr(o.civil, "id", None) == civil.id]
    assert len(minhas) >= 1
    assert any(o.id == oc.id for o in minhas)
