from usuarios.Usuario import Usuario
from Atendimento import Atendimento
from ocorrencias.Ocorrencia import Ocorrencia
from EquipeResgate import EquipeResgate
from usuarios.usuarioFactory import UsuarioFactory

usuarios = []
ocorrencias = []
atendimentos = []
equipes = []
agentes = []

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
                menuUsuario(usuario_logado, usuarios, ocorrencias, atendimentos, equipes)
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
 
def menuUsuario(usuario, usuarios, lista_ocorrencias, lista_atendimentos, lista_equipes):
    while True:
        print(f"\nUsuário: {usuario.nome} | Cargo/Tipo: {getattr(usuario, 'cargo', usuario.tipo)}")
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
                print("\nEncaminhar para Resgate")
            elif opcao == "5":
                print("\nEmitir Alerta Geral")

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

    dados = {
        "nome": input("Nome: "),
        "cpf": input("CPF: "),
        "telefone": input("Telefone: "),
        "email": input("Email: "),
        "senha": input("Senha: ")
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

if __name__ == "__main__":
    menuPrincipal()