# Sistema Bancário com Python

import textwrap

def menu():
    menu = """
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nu] Criar usuário
    [nc] Criar conta
    [lc] Listar contas
    [q]  Sair

    => """
    return input(textwrap.dedent(menu))

# Função para Depósito
def depositar(saldo, valor, extrato, /):
      print(" DEPOSITAR ".center(100, "="))
     
      if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

        print(f"Depósito no valor de R$ {valor:.2f} realizado com sucesso!")
        print("".center(100, "="))

      else:
        print("Operação falhou! Quantia insuficiente para depósito.")
        print("".center(100, "="))

      return saldo, extrato

# Função para Saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    print(" SACAR ".center(100, "="))          
    excedeu_saldo = saldo < valor
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
      print("Saque negado! Saldo insuficiente para saque.")
      print("".center(100, "="))

    elif excedeu_limite:
      print("Saque negado! O limite de saque foi ultrapassado.")
      print("".center(100, "="))

    elif excedeu_saques:
      print("Saque negado! O limite de saques diários foi alcançado.")
      print("".center(100, "="))
          
    elif valor > 0:
      saldo -= valor
      extrato += f"Saque: R$ {valor:.2f}\n"
      numero_saques += 1

      print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso!")
      print("".center(100, "="))

    else:
      print("Operação falhou! A quantia informada é inválida.")
      print("".center(100, "="))    

    return saldo, extrato, numero_saques

# Função para Exibir Extrato
def exibir_extrato(saldo, /, *, extrato):
    print(" EXTRATO ".center(100, "="))
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("".center(100, "="))
    return saldo, extrato

# Cadastra usuários
def criar_usuario(usuarios):
    print(" CRIAR USUÁRIO ".center(100, "="))
    cpf = int(input("Insira seu CPF (somente números): "))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
       print("""\n
             Operação falhou! O sistema já possui 
             um usuário com o CPF informado.
            """)
       return
    nome = input("Insira e seu nome completo: ")
    data_nascimento = input("Insira sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Insira o seu endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    print("".center(100, "="))

    usuarios.append({"nome": nome, "data_nascimento":data_nascimento, "cpf":cpf, "endereco":endereco})
    
# Filtra usuários cadastrados por CPF    
def filtrar_usuario(cpf, usuarios):
   usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
   return usuario_filtrado[0] if usuario_filtrado else None

# Cria contas bancárias para usuários cadastrados 
def criar_conta(agencia, numero_conta, usuarios):
    print(" CRIAR CONTA ".center(100, "="))
    cpf = int(input("Insira seu CPF (somente números): "))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
       print(" Conta criada com sucesso! ".center(100, "="))
       return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario }
    
    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")
    print("".center(100, "="))

# Lista de contas cadastradas
def listar_contas(contas):
   for conta in contas:
      linha = f"""\
          Agência:\t{conta['agencia']}
          C\C:\t\t{conta['numero_conta']}
          Titular:\t{conta['usuario']['nome']}
              
      """
      print("".center(100, "="))
      print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    extrato = ""
    limite = 500
    numero_saques = 0
    contas = []
    usuarios = []

    while True :
        opcao = menu()

        # Condição para depósito
        if opcao == "d":
          valor = float(input("Insira a quantia que deseja depositar: "))

          saldo, extrato = depositar(saldo, valor, extrato)

        # Condição para saque 
        elif opcao == "s":
          valor = float(input("Insira a quantia que deseja sacar: "))

          saldo, extrato, numero_saques = sacar(
             saldo=saldo, 
             valor=valor, 
             extrato=extrato, 
             limite=limite, 
             numero_saques=numero_saques, 
             limite_saques=LIMITE_SAQUES
          )

        # Condição para extrato
        elif opcao == "e":
          saldo, extrato = exibir_extrato(saldo, extrato=extrato)
        
        # Condição para criar usuário
        elif opcao == "nu":
          criar_usuario(usuarios)

        # Condição para criar conta
        elif opcao == "nc":
          numero_conta= len(contas) + 1
          conta = criar_conta(AGENCIA, numero_conta, usuarios)
        
          if conta:
              contas.append(conta)

        # Condição para listar contas 
        elif opcao == "lc":
           listar_contas(contas)

        # Condição para depósito
        elif opcao == "q":
          break

        else:
          print("\nOperação inválida! Por favor, selecione novamente a opção desejada.")
main()
