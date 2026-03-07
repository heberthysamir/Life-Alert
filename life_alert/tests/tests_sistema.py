import pytest
from domain.PerfilMedico import PerfilMedico
from domain.Atendimento import Atendimento
from domain.Alerta import Alerta
from domain.Resgate import Resgate
from domain.EquipeResgate import EquipeResgate
from domain.Vitima import Vitima
from application.atendimentoService import AtendimentoService

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

def test_rn009_nao_deve_finalizar_resgate_com_vitima_desaparecida(ocorrencia_padrao):
    vitima = Vitima(nome="João", idade="20", situacao="desaparecida", ocorrencia=ocorrencia_padrao)
    ocorrencia_padrao.vitimas.append(vitima)
    
    resgate = Resgate(id=1, ocorrencia=ocorrencia_padrao, dataInicio="2026-03-07", descricao="Busca", dataFim=None, qtdResgatados=0)

    resultado = resgate.concluirResgate()

    assert "Não é possível concluir" in resultado
    assert ocorrencia_padrao.status != "Finalizada"

def test_deve_finalizar_resgate_se_vitimas_seguras(ocorrencia_padrao):
    vitima = Vitima(nome="Maria", idade="30", situacao="Estável", ocorrencia=ocorrencia_padrao)
    ocorrencia_padrao.vitimas.append(vitima)
    
    resgate = Resgate(id=2, ocorrencia=ocorrencia_padrao, dataInicio="2026-03-07", descricao="Resgate normal", dataFim=None, qtdResgatados=1)

    resultado = resgate.concluirResgate()

    assert "Resgate finalizado" in resultado
    assert ocorrencia_padrao.status == "Finalizada"

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
    resgate = Resgate(id=10, ocorrencia=ocorrencia_padrao, dataInicio="2026-03-07", descricao="Busca e Salvamento", dataFim=None, qtdResgatados=0)
    
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