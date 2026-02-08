from life_alert.Usuario import Usuario, Civil, Atendente, Agente

usuarios = []  
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
                menuUsuario(usuario_logado)
        elif opcao == "2":
            Usuario.criarUsuario(usuarios)
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida")

def menuUsuario(usuario):
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
        if opcao == "1":
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
        if opcao == "2":
            confirmacao = input("Tem certeza que deseja excluir sua conta? (sim/não): ")
            if confirmacao.lower() == 'sim':
                removido = usuario.excluirUsuario(usuarios)
                if removido:
                    print("Conta excluída com sucesso.")
                    return 
                else:
                    print(f"\nUsuário não encontrado")

if __name__ == "__main__":
    menuPrincipal()
