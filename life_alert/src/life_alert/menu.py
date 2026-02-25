from datetime import datetime
from usuarios.Usuario import Usuario
from Atendimento import Atendimento
from ocorrencias.Ocorrencia import Ocorrencia
from EquipeResgate import EquipeResgate
from application.usuariosFactory import UsuarioFactory
from application.alertasFactory import AlertaFactory

usuarios = []
ocorrencias = []
atendimentos = []
equipes = []
agentes = []
alertas = []

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
                menuUsuario(usuario_logado, usuarios, ocorrencias, atendimentos, equipes, alertas)
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
            print(f"\n --- Gestão da equipe {equipeSelecionada.id} ({equipeSelecionada.especialidade}) --- \n")
            print("1 - Adicionar Agente")
            print("2 - Remover Agente")
            print("3 - Atualizar Status de Agente")
            print("4 - Listar Membros")
            print("0 - Voltar")
            cmd = input("Insira a opção desejada: \n")

            if cmd == "1":
                equipeSelecionada.adicionarMembro(lista_usuarios)
            elif cmd == "2":
                equipeSelecionada.removerMembro()
            elif cmd == "3":
                equipeSelecionada.atualizarStatusMembro()
            elif cmd == "4":
                equipeSelecionada.listarMembros()
            elif cmd == "0":
                break
            else:
                print("Opção inválida, tente novamente.")
 
def menuUsuario(usuario, usuarios, lista_ocorrencias, lista_atendimentos, lista_equipes, lista_alerta):
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
                ocorrencia = Ocorrencia.abrirOcorrencia(usuarios, usuario)
                if ocorrencia:
                    lista_ocorrencias.append(ocorrencia)
            elif opcao == "4":
                print("\nMinhas Ocorrências:")
                minhas_ocorrencias = [o for o in lista_ocorrencias if o.civil == usuario]
                if not minhas_ocorrencias:
                    print("Você não tem ocorrências registradas.")
                else:
                    for o in minhas_ocorrencias:
                        print(o)

        elif usuario.tipo == "Atendente":
            if opcao == "3":
                atendimento = Atendimento.iniciarAtendimento(usuarios, lista_ocorrencias, usuario)
                if atendimento:
                    lista_atendimentos.append(atendimento)
            elif opcao == "4":
                Atendimento.encaminharResgate(lista_equipes, lista_ocorrencias)
            elif opcao == "5":
                print("1 - Criar Alerta")
                print("2 - Cancelar Alerta")
                sub_opcao = input("Escolha: ")
                if sub_opcao == "1":
                    criarAlerta(alertas, ocorrencias)
                elif sub_opcao == "2":
                    cancelarAlerta(alertas)
                else:
                    print("Opção inválida.")

        elif usuario.tipo == "Agente":
            if opcao == "3":
                print("\nGerenciar Resgate em Andamento")
            elif opcao == "4":
                print("\nCadastrar Vítima")
            elif usuario.cargo.lower() == "lider":
                if opcao == "5":
                    EquipeResgate.cadastrarEquipe(lista_equipes, usuario)
                elif opcao == "6":
                    menuEquipe(lista_equipes, usuarios, usuario)
                elif opcao == "7":
                    EquipeResgate.listarEquipes(lista_equipes)

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

if __name__ == "__main__":
    menuPrincipal()