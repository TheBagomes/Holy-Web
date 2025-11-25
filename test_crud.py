from models.user import User
from database import criar_tabelas

criar_tabelas()

# ================================
# FUNÇÕES DO CRUD
# ================================

def listar_usuarios():
    usuarios = User.get_all()
    if not usuarios:
        print("\nNenhum usuário encontrado.\n")
        return
    
    print("\n=== LISTA DE USUÁRIOS ===")
    for u in usuarios:
        print(f"ID: {u.id} | Nome: {u.nome} | Email: {u.email} | Senha: {u.senha}")
    print()


def criar_usuario():
    print("\n=== CRIAR NOVO USUÁRIO ===")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")

    novo = User(None, nome, email, senha)
    novo.save()

    print("\n✔ Usuário criado com sucesso!\n")


def editar_usuario():
    print("\n=== EDITAR USUÁRIO ===")
    try:
        user_id = int(input("ID do usuário que deseja editar: "))
    except:
        print("ID inválido!")
        return

    user = User.get(user_id)
    if not user:
        print("\nUsuário não encontrado!\n")
        return

    print(f"\nDeixe vazio para manter o valor atual.\n")

    nome = input(f"Nome atual ({user.nome}): ") or user.nome
    email = input(f"Email atual ({user.email}): ") or user.email
    senha = input(f"Senha atual ({user.senha}): ") or user.senha

    user = User(user_id, nome, email, senha)
    user.update()

    print("\n✔ Usuário atualizado com sucesso!\n")


def deletar_usuario():
    print("\n=== REMOVER USUÁRIO ===")
    try:
        user_id = int(input("ID do usuário que deseja remover: "))
    except:
        print("ID inválido!")
        return

    user = User.get(user_id)
    if not user:
        print("\nUsuário não encontrado!\n")
        return

    confirm = input(f"Tem certeza que deseja remover '{user.nome}'? (s/n): ").lower()

    if confirm == "s":
        User.delete(user_id)
        print("\n✔ Usuário removido com sucesso!\n")
    else:
        print("\nOperação cancelada.\n")


# ================================
# MENU INTERATIVO
# ================================

def menu():
    while True:
        print("\n=========== MENU CRUD ===========")
        print("1 - Listar usuários")
        print("2 - Criar novo usuário")
        print("3 - Editar usuário existente")
        print("4 - Remover usuário")
        print("0 - Sair")
        print("==================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_usuarios()
        elif opcao == "2":
            criar_usuario()
        elif opcao == "3":
            editar_usuario()
        elif opcao == "4":
            deletar_usuario()
        elif opcao == "0":
            print("\nSaindo...\n")
            break
        else:
            print("\nOpção inválida! Tente novamente.\n")


# ================================
# EXECUTAR O MENU
# ================================
menu()
