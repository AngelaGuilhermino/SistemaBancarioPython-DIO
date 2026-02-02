# Sistema Bancário com Python

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
extrato = ""
limite = 500
LIMITE_SAQUES = 3
numero_saques = 0

while True :

    opcao = input(menu)

    if opcao == "d":
      print(" Depositar ".center(40, "="))

      valor = float(input("Insira a quantia que deseja depositar: "))

      if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

        print(f"Depósito no valor de R$ {valor:.2f} realizado com sucesso!\n")

      else:
        print("Operação falhou! Quantia insuficiente para depósito.")

    elif opcao == "s":
      print(" Sacar ".center(40, "="))

      valor = float(input("Insira a quantia que deseja sacar: "))
      
      excedeu_saldo = saldo < valor
      excedeu_limite = valor > limite
      excedeu_saques = numero_saques >= LIMITE_SAQUES

      if excedeu_saldo:
        print("Saque negado! Saldo insuficiente para saque.")

      elif excedeu_limite:
        print("Saque negado! O limite de saque foi ultrapassado.")

      elif excedeu_saques:
        print("Saque negado! O limite de saques diários foi alcançado.")
      
      elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

        print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso!\n")

      else:
        print("Operação falhou! A quantia informada é inválida.")


    elif opcao == "e":
      print(" Extrato ".center(40, "="))
      print("Não foram realizadas movimentações." if not extrato else extrato)
      print(f"\nSaldo: R$ {saldo:.2f}")
      print("".center(40, "="))

    elif opcao == "q":
      break

    else:
      print("\nOperação inválida! Por favor, selecione novamente a opção desejada.")