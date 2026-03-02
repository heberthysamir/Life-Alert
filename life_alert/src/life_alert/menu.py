from datetime import datetime
from domain.usuarios.Usuario import Usuario
from domain.Atendimento import Atendimento
from domain.EquipeResgate import EquipeResgate
from domain.Resgate import Resgate
from application.usuariosFactory import UsuarioFactory
from application.alertasFactory import AlertaFactory
from application.equipeFactory import EquipeFactory
from application.ocorrenciaFactory import OcorrenciaFactory
from application.perfilMedicoFactory import PerfilMedicoFactory
from application.vitimaFactory import VitimaFactory
from application.atendimentoService import AtendimentoService
from application.relatorioService import RelatorioService

usuarios = []
ocorrencias = []
atendimentos = []
equipes = []
agentes = []
alertas = []
vitimas = []
resgates = []

def menuPrincipal():
    while True:
        print("\nLIFE ALERT")
        print("1 - Fazer login")
        print("2 - Criar usuário")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            Usuario.listarUsuarios(usuarios)
            usuario_logado = Usuario.Login(usuarios)
            if usuario_logado:
                menuUsuario(usuario_logado, usuarios, ocorrencias, atendimentos, equipes, alertas, vitimas)
        elif opcao == "2":
            criarUsuario(usuarios)
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida")

def menuEquipe(lista_equipes, lista_usuarios, usuario_logado):
        print(f"\n --- Gerenciar equipes (Líder: {usuario_logado.nome}) ---\n")

        minhasEquipes = [e for e in lista_equipes if usuario_logado in e.agentes]

        if not minhasEquipes:
            print("Você não está cadastrado em nenhuma equipe.")
            return
        
        print("\nSuas equipes cadastradas: \n")
        for equipe in minhasEquipes:
            print(equipe)
        
        idEquipe = input("Digite o ID da equipe à gerenciar: \n")
        equipeSelecionada = next((e for e in minhasEquipes if str(e.id) == idEquipe), None)

        if not equipeSelecionada: 
            print("Equipe não encontrada ou você não tem permissão para gerenciá-la")
            return
        
        while True:
            print(f"\nGestão da equipe {equipeSelecionada.id} ({equipeSelecionada.especialidade}) --- \n")
            print("1 - Adicionar Agente")
            print("2 - Remover Agente")
            print("3 - Atualizar Status de Agente")
            print("4 - Listar Membros")
            print("0 - Voltar")
            cmd = input("Insira a opção desejada: \n")

            if cmd == "1":
                agentes_disponiveis = [u for u in lista_usuarios if u.tipo == "Agente" and u not in equipeSelecionada.agentes]
                
                if not agentes_disponiveis:
                    print("\nNão há agentes disponíveis para adicionar.")
                else:
                    print("\n--- Agentes Disponíveis ---")
                    for a in agentes_disponiveis:
                        print(f"[{a.id}] {a.nome} ({a.cargo})")
                    
                    id_alvo = input("\nDigite o ID do agente que deseja inserir: ")
                    agente_escolhido = next((u for u in agentes_disponiveis if str(u.id) == id_alvo), None)
                    
                    if agente_escolhido:
                        equipeSelecionada.adicionar_membro(agente_escolhido)
                        print(f"✅ Agente {agente_escolhido.nome} adicionado com sucesso!")
                    else:
                        print("❌ ID inválido ou agente não disponível.")

            elif cmd == "2":
                equipeSelecionada.listarMembros()
                id_remover = input("\nDigite o ID do membro que deseja remover: ")
                
                try:
                    equipeSelecionada.remover_membro(int(id_remover))
                    print("✅ Membro removido da equipe.")
                except ValueError as e:
                    print(f"❌ Erro: {e}")

            elif cmd == "3":
                equipeSelecionada.listarMembros()
                id_status = input("\nDigite o ID do membro para atualizar: ")
                novo_status = input("Novo Status (ex: Disponível, Em Resgate, Licença): ")
                
                try:
                    equipeSelecionada.alterar_status_agente(int(id_status), novo_status)
                    print("✅ Status do membro atualizado!")
                except ValueError as e:
                    print(f"❌ Erro: {e}")

            elif cmd == "4":
                print(f"\n--- Membros da Equipe {equipeSelecionada.id} ---")
                equipeSelecionada.listarMembros()

            elif cmd == "0":
                break
            else:
                print("Opção inválida, tente novamente.")
 
def menuUsuario(usuario, usuarios, lista_ocorrencias, lista_atendimentos, lista_equipes, lista_alerta, lista_vitimas):
    while True:
        print(f"\nUsuário: {usuario.nome} | Cargo/Tipo: {getattr(usuario, 'cargo', usuario.tipo)}")
        mostrarAlertas(usuario, lista_alerta)
        usuario.exibirMenu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "0":
            break

        elif opcao == "1":
            print("\nAtualizar Dados:")
            novo_nome = input("Novo nome (ou Enter para manter): ")
            novo_tel = input("Novo telefone (ou Enter para manter): ")
            novo_email = input("Novo e-mail (ou Enter para manter): ")
            nova_senha = input("Nova senha (ou Enter para manter): ")
            usuario.atualizarUsuario(
                novo_nome=novo_nome, 
                novo_telefone=novo_tel, 
                novo_email=novo_email, 
                nova_senha=nova_senha
            )

        elif opcao == "2":
            confirmacao = input("Tem certeza que deseja excluir sua conta? (sim/não): ")
            if confirmacao.lower() == 'sim':
                removido = usuario.excluirUsuario(usuarios)
                if removido:
                    print("Conta excluída com sucesso.")
                    return 
                else:
                    print(f"\nUsuário não encontrado")

        elif usuario.tipo == "Civil":
            if opcao == "3":
                ocorrencia = criarOcorrencia(usuario)
                if ocorrencia:
                    lista_ocorrencias.append(ocorrencia)
                atendente = AtendimentoService.designarAtendente(ocorrencia, usuarios, lista_atendimentos)
                if atendente:
                    novo_atendimento = Atendimento(atendente=atendente, ocorrencia=ocorrencia)
                    lista_atendimentos.append(novo_atendimento)
                    ocorrencia.status = "Em Atendimento"
                    print(f"Ocorrência enviada para o atendente: {atendente.nome}")
                else:
                    print("Ocorrência registrada. Aguardando atendente disponível na sua cidade.")

            elif opcao == "4":
                print("\nMinhas Ocorrências:")
                minhas_ocorrencias = [o for o in lista_ocorrencias if o.civil == usuario]
                if not minhas_ocorrencias:
                    print("Você não tem ocorrências registradas.")
                else:
                    for o in minhas_ocorrencias:
                        print(o)

            elif opcao == "5":
                while True:
                    print("\nGerenciamento do perfil médico:")
                    print("0 - Voltar")
                    print("1 - Visualizar perfil")
                    print("2 - Cadastrar perfil")
                    print("3 - Atualizar perfil")

                    sub_opcao = input("\nEscolha uma opção: ")

                    if sub_opcao == "1":
                        if usuario.perfil_medico is None:
                            print("\nVocê ainda não possui um perfil cadastrado.")
                        else:
                            print(usuario.perfil_medico)
                    elif sub_opcao == "2":
                        cadastrarPerfilMedicoMenu(usuario)
                    elif sub_opcao == "3":
                        if usuario.perfil_medico is None:
                            print("\nVocê ainda não possui um perfil cadastrado.")
                        else:
                            atualizarPerfilMedicoMenu(usuario)
                    elif sub_opcao == "0":
                        break
                    else:
                        print("Opção inválida.")

        elif usuario.tipo == "Atendente":
            if opcao == "3":
                meus_atendimentos = [a for a in lista_atendimentos if a.atendente == usuario]
                if not meus_atendimentos:
                    print("\nVocê não possui atendimentos designados.")
                else:
                    print("\nSEUS ATENDIMENTOS:")
                    for i, at in enumerate(meus_atendimentos):
                        print(f"[{i}] {at}")
                    
                    escolha = input("\nSelecione o índice para gerenciar (ou 's' para sair): ")
                    if escolha.isdigit() and int(escolha) < len(meus_atendimentos):
                        at_sel = meus_atendimentos[int(escolha)]
                        at_sel.atualizarAtendimento()

            elif opcao == "4":
                Atendimento.encaminharResgate(lista_equipes, lista_ocorrencias)
            elif opcao == "5":
                print("1 - Criar Alerta")
                print("2 - Cancelar Alerta")
                sub_opcao = input("Escolha: ")
                if sub_opcao == "1":
                    criarAlerta(alertas, lista_ocorrencias)
                elif sub_opcao == "2":
                    cancelarAlerta(alertas)
                else:
                    print("Opção inválida.")

        elif usuario.tipo == "Agente":
            if opcao == "3":
                if not lista_vitimas:
                    print("\nNenhuma vítima cadastrada no sistema.")
                else:
                    print("\nGERENCIAR VÍTIMAS:")
                    for i, v in enumerate(lista_vitimas):
                        print(f"[{i}] {v}")
                    
                    escolha = input("\nÍndice para atualizar (ou 's' para sair): ")
                    if escolha.isdigit() and int(escolha) < len(lista_vitimas):
                        vitima_sel = lista_vitimas[int(escolha)]
                        nova_sit = input(f"Nova situação para {vitima_sel.nome}: ")
                        if vitima_sel.atualizar_situacao(nova_sit):
                            print("✅ Situação atualizada!")

            elif opcao == "4":
                nova_v = cadastrarVitimaMenu(lista_ocorrencias)
                if nova_v:
                    lista_vitimas.append(nova_v)
                    print(f"✅ Vítima {nova_v.nome} registrada.")
                    
            elif usuario.cargo.lower() == "lider":
                if opcao == "5":
                    nova_equipe = criarEquipeMenu(usuario)
                    if nova_equipe:
                        lista_equipes.append(nova_equipe)
                elif opcao == "6":
                    menuEquipe(lista_equipes, usuarios, usuario)
                elif opcao == "7":
                    menuRelatorio(lista_ocorrencias)
                elif opcao == "8":
                    gerenciarResgates(usuario, lista_ocorrencias, atendimentos)

def criarUsuario(lista_usuarios):
    print("\nCRIAR NOVO USUÁRIO")
    print("1 - Civil")
    print("2 - Atendente")
    print("3 - Agente")

    tipo = input("Escolha o tipo: ")

    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")
    rua = input("Rua: ")
    num = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    email = input("Email: ")
    senha = input("Senha: ")

    dados = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "rua": rua,
        "num": num, 
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "email": email,
        "senha": senha
    }

    if tipo == "2":
        dados["turno"] = input("Turno: ")

    elif tipo == "3":
        dados["cargo"] = input("Cargo (Ex: Líder, Operacional): ")
        dados["status"] = True 

    try:
        usuario = UsuarioFactory.criar(tipo, **dados)
        lista_usuarios.append(usuario)
        print(f"\n{usuario.tipo} '{usuario.nome}' criado com sucesso!")
        
    except ValueError as e:
        print(f"\nErro: {e}")
    except TypeError as e:
        print(f"\nErro de Atributo: Verifique se os campos extras estão corretos nas subclasses.")
        print(f"Detalhe técnico: {e}")

def criarAlerta(lista_alertas, lista_ocorrencias):
    if not lista_ocorrencias:
        print("\nNão há ocorrências registradas para gerar alertas.")
        return

    print("\nSELECIONE UMA OCORRÊNCIA PARA GERAR O ALERTA")
    for i, oc in enumerate(lista_ocorrencias):
        print(f"{i} - [{oc.tipo}] em {oc.bairro}, {oc.cidade}")

    try:
        idx = int(input("\nEscolha o número da ocorrência: "))
        ocorrencia_base = lista_ocorrencias[idx]
        
        print(f"\nGerando alerta para: {ocorrencia_base.tipo} em {ocorrencia_base.rua}")
        
        titulo = input("Título do Alerta (Ex: Perigo de Alagamento): ")
        msg = input("Mensagem de orientação: ")
        
        print("\nAlcance do Alerta:")
        print("1 - Cidade Toda | 2 - Bairro | 3 - Rua")
        op_escopo = input("Escolha o alcance: ")
        
        escopos = {"1": "cidade", "2": "bairro", "3": "rua"}
        escopo_final = escopos.get(op_escopo, "cidade")

        dados = {
            "titulo": titulo,
            "mensagem": msg,
            "ocorrencia": ocorrencia_base,
            "escopo": escopo_final,
            "horario": datetime.now().strftime("%H:%M:%S")
        }

        novo_alerta = AlertaFactory.criar_alerta(**dados)
        lista_alertas.append(novo_alerta)
        print("\n✅ Alerta disparado com sucesso baseado na ocorrência selecionada!")

    except (ValueError, IndexError):
        print("\n❌ Seleção inválida. Operação cancelada.")

def cancelarAlerta(lista_alertas):
    if not lista_alertas:
        print("\nNão existem alertas ativos no sistema para cancelar.")
        return

    print("\nAlertas Ativos:")
    for i, alerta in enumerate(lista_alertas):
        print(f"ID: {i} | {alerta.titulo} ({alerta.horario})")

    try:
        escolha = int(input("\nDigite o ID do alerta que deseja cancelar: "))
        
        if 0 <= escolha < len(lista_alertas):
            alerta_removido = lista_alertas.pop(escolha)
            print(f"\nAlerta '{alerta_removido.titulo}' cancelado com sucesso!")
        else:
            print("\nID inválido.")
            
    except ValueError:
        print("\nPor favor, digite um número válido.")

def mostrarAlertas(usuario_logado, lista_alerta):
    print(f"\n🔔 --- CENTRAL DE ALERTAS: {usuario_logado.cidade.upper()} ---")
    encontrou = False

    for alerta in lista_alerta :
        oc = alerta.ocorrencia 
        mostrar = False

        if alerta.escopo == "cidade":
            if oc.cidade.lower() == usuario_logado.cidade.lower():
                mostrar = True

        elif alerta.escopo == "bairro":
            if (oc.cidade.lower() == usuario_logado.cidade.lower() and 
                oc.bairro.lower() == usuario_logado.bairro.lower()):
                mostrar = True

        elif alerta.escopo == "rua":
            if (oc.cidade.lower() == usuario_logado.cidade.lower() and 
                oc.bairro.lower() == usuario_logado.bairro.lower() and
                oc.rua.lower() == usuario_logado.rua.lower()):
                mostrar = True

        if mostrar:
            print("-" * 40)
            print(alerta) 
            encontrou = True

    if not encontrou:
        print("Nenhum alerta no momento\n")
    print("-" * 40)

def criarOcorrencia(
        usuario_logado):
    print("\nABERTURA DE OCORRÊNCIA:")
    print("1 - Policial")
    print("2 - Médica")
    print("3 - Incêndio")
    print("4 - Enchente")
    print("5 - Outros(especificar na descrição)")
    
    opcao = input("Selecione o tipo: ")
    
    tipos_nomes = {"1": "Policial", "2": "Médica", "3": "Incêndio", "4": "Enchente", "5": "Outros"}
    tipo_selecionado = tipos_nomes.get(opcao, "Geral")

    dados = {
        "atendente": None,
        "agente": None,
        "civil": usuario_logado,
        "dataHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Aberta",
        "descricao": input("Descrição detalhada: "),
        "rua": input("Rua: "),
        "bairro": input("Bairro: "),
        "cidade": input("Cidade: "),
        "estado": input("Estado: "),
        "complemento": input("Complemento: "),
        "gravidade": input("Gravidade (baixa/média/alta): "),
        "tipo": tipo_selecionado,
        "qtdAfetados": int(input("Qtd de pessoas afetadas: ")),
        "equipe": None
    }

    if opcao == "1":
        dados["tipoCrime"] = input("Tipo de crime: ")
        dados["qtdCriminosos"] = int(input("Qtd de criminosos: "))
        dados["descricaoSuspeito"] = input("Descrição do suspeito: ")
        
    elif opcao == "2":
        dados["perfilMedico"] = input("Perfil médico (Ex: Diabético, Idoso): ")
        dados["sintomas"] = input("Sintomas observados: ")
    try:
        nova_oc = OcorrenciaFactory.criar(opcao, **dados)
        print(f"\nOcorrência de {nova_oc.tipo} registrada (ID: {nova_oc.id})!")
        return nova_oc
    except Exception as e:
        print(f"Erro ao registrar: {e}")
        return None

def criarEquipeMenu(usuario_logado):
    print("\nCADASTRAR NOVA EQUIPE:")
    localidade = input("Localidade da base: ")
    setor = input("Setor (ex: SAMU, PM, Bombeiros): ")
    especialidade = input("Especialidade (ex: Resgate Aquático, Incêndio): ")
    
    try:
        equipe = EquipeFactory.criar_equipe(usuario_logado, localidade, setor, especialidade)
        print(f"✅ Equipe {equipe.id} cadastrada com sucesso!")
        return equipe
    except Exception as e:
        print(f"❌ Erro ao criar equipe: {e}")
        return None

def cadastrarPerfilMedicoMenu(usuario_civil):
    if usuario_civil.perfil_medico is not None:
        print("\nVocê já possui um perfil médico cadastrado.")
        return

    print("\nCADASTRO DE PERFIL MÉDICO:")
    alergias = input("Alergias (ou Enter para 'Nenhuma'): ")
    doencas = input("Doenças (ou Enter para 'Nenhuma'): ")
    deficiencia = input("Deficiências (ou Enter para 'Nenhuma'): ")
    tipo = input("Tipo Sanguíneo (ou Enter para 'Desconhecido'): ")

    novo_perfil = PerfilMedicoFactory.criar(alergias, doencas, deficiencia, tipo)
    usuario_civil.perfil_medico = novo_perfil
    print("Perfil Médico cadastrado com sucesso.")

def atualizarPerfilMedicoMenu(usuario_civil):
    if usuario_civil.perfil_medico is None:
        print("\nNenhum perfil encontrado para atualizar.")
        return

    perfil = usuario_civil.perfil_medico
    print("\nATUALIZAÇÃO DE PERFIL MÉDICO:")
    print("(Pressione Enter para manter a informação atual)")

    nova_alergia = input(f"Alergias [{perfil.alergias}]: ")
    nova_doenca = input(f"Doenças [{perfil.doencas}]: ")
    nova_deficiencia = input(f"Deficiência [{perfil.deficiencia}]: ")
    novo_tipo = input(f"Tipo Sanguíneo [{perfil.tipoSanguineo}]: ")

    perfil.atualizar_dados(nova_alergia, nova_doenca, nova_deficiencia, novo_tipo)
    print("Perfil médico atualizado.")

def cadastrarVitimaMenu(lista_ocorrencias):
    print("\nCADASTRAR VÍTIMA NO LOCAL:")
    if not lista_ocorrencias:
        print("Nenhuma ocorrência ativa para vincular a vítima.")
        return None

    for i, oc in enumerate(lista_ocorrencias):
        print(f"[{i}] {oc.tipo} - {oc.bairro}")
    
    try:
        idx = int(input("Vincular à ocorrência (índice): "))
        oc_selecionada = lista_ocorrencias[idx]
        
        nome = input("Nome da vítima: ")
        idade = input("Idade: ")
        situacao = input("Situação (ex: Estável, Grave, Óbito): ")

        nova_v = VitimaFactory.criar(nome, idade, situacao, oc_selecionada)
        return nova_v
    except (ValueError, IndexError):
        print("Seleção inválida.")
        return None

def menuRelatorio(lista_ocorrencias):
    print("\nGERAR RELATÓRio:")
    data_i = input("Data Inicial (DD/MM/AAAA): ")
    data_f = input("Data Final (DD/MM/AAAA): ")
    
    try:
        relatorio = RelatorioService.gerar_estatisticas(lista_ocorrencias, data_i, data_f)
        relatorio.exibir()
        
    except ValueError:
        print("❌ Formato de data inválido. Use DD/MM/AAAA.")


def gerenciarResgates(usuario_logado, lista_ocorrencias, lista_resgates):
    print(f"--- Gerenciando resgates - Líder: {usuario_logado.nome} ---")
    
    minhasOcorrencias = [
        o for o in lista_ocorrencias 
        if o.equipe and usuario_logado in o.equipe.agentes and usuario_logado.cargo.lower() == "lider"
    ]

    if not minhasOcorrencias:
        print("Você não possui ocorrências em andamento sob sua liderança.")
        return

    for i, oc in enumerate(minhasOcorrencias):
        print(f"{i} - Tipo: {oc.tipo}, Status: {oc.status}")

    try: 
        index = int(input("Selecione o índice da ocorrência para gerenciar (ou 's' para voltar): "))
        ocSel = minhasOcorrencias[index]

        while True:
            print(f"\nGerenciando Resgate - Ocorrencia #{ocSel.id}")
            print("1 - Iniciar Resgate")
            print("2 - Adicionar Resgatados")
            print("3 - Concluir Resgate")
            print("0 - Voltar")

            cmd = input("Escolha uma opção: ")

            if cmd == "1":
                if any(r.ocorrencia == ocSel for r in lista_resgates):
                    print("❌ Resgate já iniciado para esta ocorrência.")
                else:
                    desc = input("Descrição do plano de resgate: ")
                    newResgate = Resgate(ocSel.id, ocSel, desc)
                    lista_resgates.append(newResgate)
                    ocSel.status = "Em Resgate"
                    print(f"✅ Resgate iniciado para Ocorrência #{ocSel.id}, às {newResgate.dataInicio}.")
            
            elif cmd == "2":
                resgateAtual = next((r for r in lista_resgates if r.ocorrencia == ocSel), None) 
                if resgateAtual:
                    qtd = int(input("Informe a quantidade de resgatados no momento: "))
                    print(resgateAtual.adicionarVitima(qtd))
                else:
                    print("❌ Nenhum resgate iniciado para esta ocorrência.")

            elif cmd == "3":
                resgateAtual = next((r for r in lista_resgates if r.ocorrencia == ocSel), None)
                if resgateAtual:
                    print(resgateAtual.concluirResgate())
                else:
                    print("❌ Nenhum resgate iniciado para esta ocorrência.")
                
            elif cmd == "0":
                break
    except (ValueError, IndexError):
        print("Seleção inválida. Retornando ao menu principal.")



if __name__ == "__main__":
    menuPrincipal()