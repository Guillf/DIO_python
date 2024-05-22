#/t serve para deixar tabulado

import textwrap

def menu():
  menu = """\n
  ============== MENU ==============
  [d] \t Depositar
  [s] \t Sacar
  [e] \t Extrato
  [nc] \t Nova conta
  [lc] \t Listar contas
  [nu] \t Novo usuário
  [q] \t Sair
  ===================================
  """
  return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato,/):
  if valor > 0:
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print("\n=== Depósito realizado com sucesso! ===")
  else:
    print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

  return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques,limite_saques):
  excedeu_saldo = valor > saldo
  excedeu_limite = valor > limite
  excedeu_saques = numero_saques >= LIMITE_SAQUES

  if excedeu_saldo:
    print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

  elif excedeu_limite:
    print(f"\n@@@ Operação falhou! O valor do saque (R$ {valor:.2f}) excede o limite. @@@")

  elif excedeu_saques:
    print("\n@@@ Operação falhou! Você atingiu o número máximo de saques diários. @@@")

  elif valor > 0:
    saldo -= valor
    extrato += f"Saque:\t\tR$ {valor:.2f}\n"
    numero_saques +=1
    print("\n=== Saque realizado com sucesso! ===")

  else:
    print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

  return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
  print("\n========== Extrato ==========")
  print("Não foram realizadas movimentações" if not extrato else extrato)
  print(f"\nSaldo: R$ {saldo:.2f}")
  print("===============================")

def criar_usuario(usuarios):
  cpf = input("Informe o CPF (somente números): ")
  usuario = filtar_usuarios(cpf, usuarios)

  if usuario:
    print(f"\n@@@ Usuário já cadastrado com o CPF {cpf}. @@@")
    return

  nome = input(f"Informe o nome completo do usuário: ")
  data_nascimento = input(f"Informe a data de nascimento do usuário no formato dd-mm-aaaa: ")
  endereco = input(f"Informe o endereço do usuário no formato (logradouro, número - bairro - cidade/sigla do estado): ")

  usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
  print(f"\n=== Usuário cadastrado com sucesso! ===")

def filtar_usuarios(cpf, usuarios):
  usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
  return usuarios_filtrados[0] if usuarios_filtrados else None
  

def criar_conta(agencia, numero_conta, usuarios):
  cpf = input(f"Informe o CPF do usuário que deseja criar a conta (somente números): ")
  usuario = filtar_usuarios (cpf, usuarios)

  if usuario:
    print(f'\n=== Conta criada com sucesso! ===')
    return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

  print(f"\n@@@ Usuário não encontrado com o CPF {cpf}, fluxo de criação de conta encerrado. @@@")

def listar_contas(contas):
  for conta in contas:
    linha = f"""\
      Agência:\t {conta["agencia"]}
      Número da conta:\t\t {conta["numero_conta"]}
      Titular:\t {conta["usuario"]["nome"]}
    """
    print("=" * 100)
    print(textwrap.dedent(linha))

def main():
  LIMITE_SAQUES = 3
  AGENCIA = "0001"

  saldo = 0
  limite = 500
  extrato = ""
  numero_saques = 0
  usuarios = []
  contas = []

  while True:
    opcao = menu()

    if opcao == "d":
      valor = float(input(f"Informe o valor do depósito: R$ "))

      saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
      valor = float(input(f"Informe o valor do saque: R$ "))

      saldo, extrato = sacar (
        saldo = saldo,
        valor = valor,
        extrato = extrato,
        limite = limite,
        numero_saques = numero_saques,
        limite_saques = LIMITE_SAQUES,
      )

    elif opcao == "e":
      exibir_extrato(saldo, extrato = extrato)
      
    elif opcao == "nu":
      criar_usuario(usuarios)

    elif opcao == "nc":
      numero_conta = len(contas) +1 #resolve a questão do número da conta começando em 1
      conta = criar_conta(AGENCIA, numero_conta, usuarios)
      if conta:
        contas.append(conta)

    elif opcao == "lc":
      listar_contas(contas)

    elif opcao == "q":
      break

    else:
      print("Operação inválida, por favor selecione novamente a operação desejada.")

main()