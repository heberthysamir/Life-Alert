from Usuario import Usuario, Civil, Atendente, Agente
from Atendimento import Atendimento
from Ocorrencia import Ocorrencia
from EquipeResgate import EquipeResgate

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
            Usuario.criarUsuario(usuarios)
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida")

def menuUsuario(usuario, usuarios, lista_ocorrencias, lista_atendimentos, lista_equipes):
    while True:
        print(f"Usuário: {usuario.nome} | Cargo/Tipo: {getattr(usuario, 'cargo', usuario.tipo)}")
        print("0 - Logout")
        print("1 - Atualizar dados")
        print("2 - Apagar conta")
        
        if usuario.tipo == "Civil":
            print("3 - Registrar Ocorrência")
            print("4 - Acompanhar minhas Ocorrências")

        elif usuario.tipo == "Atendente":
            print("3 - Analisar Ocorrência")
            print("4 - Encaminhar para Resgate")
            print("5 - Emitir Alerta Geral")

        elif usuario.tipo == "Agente":
            print("3 - Gerenciar Resgate em Andamento")
            print("4 - Cadastrar Vítima")
            
            if usuario.cargo.lower() == "lider":
                print("5 - Cadastrar Nova Equipe de Resgate")
                print("6 - Gerenciar Membros da Equipe")
                
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
            elif opcao == "5" and usuario.cargo.lower() == "lider":
                nova_equipe = EquipeResgate.cadastrarEquipe(lista_equipes)
                if nova_equipe:
                    lista_equipes.append(nova_equipe)
            elif opcao == "6" and usuario.cargo.lower() == "lider":
                print("\nGerenciar Membros da Equipe")

if __name__ == "__main__":
    menuPrincipal()
