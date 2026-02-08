from life_alert.Usuario import Usuario, Civil, Atendente, Agente

usuarios = []  
def menu():
    while True:
        print("\nLIFE ALERT")
        print("1 - Fazer login")
        print("2 - Criar usuário")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            listar_usuarios()
        elif opcao == "2":
            criar_usuario()
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")


def listar_usuarios():
    print("\n.Usuários Cadastrados:")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(u)


def criar_usuario():
    print("\n.Criar Usuário:")
    print("1 - Civil")
    print("2 - Atendente")
    print("3 - Agente")
    opcao = input("Escolha o tipo: ")

    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    senha = input("Senha: ")

    if opcao == "1":
        usuario = Civil(nome, cpf, telefone, email, senha)

    elif opcao == "2":
        turno = input("Turno (manha/tarde/noite): ")
        usuario = Atendente(nome, cpf, telefone, email, senha, turno)

    elif opcao == "3":
        cargo = input("Cargo (lider/operacional): ")
        status = True
        usuario = Agente(nome, cpf, telefone, email, senha, cargo, status)

    else:
        print("Opção inválida!")
        return

    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

if __name__ == "__main__":
    menu()
