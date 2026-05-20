import textwrap
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from colorama import Fore, Style, init
from pathlib import Path

ROOT_PATH = Path(__file__).parent

init(autoreset=True)

class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta =self.contas[self._index]
            return conta
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0
    
    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Você excedeu o número de transações diária!")
            return
        
        transacao.registrar(conta)
    
    def adicionar_conta (self, conta):
       self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.cpf}')>"  

class Conta: 
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod 
    def nova_conta(cls, numero, cliente ): # Novos objetos serão criados de forma organizada
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = saldo < valor

        if excedeu_saldo:
            print("\nSaque negado! Saldo insuficiente para saque.")

        elif valor > 0:
            self._saldo -= valor
            print(Fore.GREEN + f"\nSaque no valor de R$ {valor:.2f} realizado com sucesso!")
            return True

        else:
            print(Fore.RED + "\nSaque negado! O valor informado é inválido.")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(Fore.GREEN + f"\nDepósito no valor de R$ {valor:.2f} realizado com sucesso!")
        
        else:
            print(Fore.RED + "\nOperação falhou! O valor informado é inválido.")
            return False
            
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, numero, cliente, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(Fore.RED + "\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print(Fore.RED + "\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)   # sacar da classe pai
        
        return False
    
    def __repr__(self):
        return f"""<{self.__class__.__name__}: ('{self.agencia}', '{self.numero},' '{self.cliente.nome}')>"""

    def __str__(self):
        return f"""
          \t  Agência: {self.agencia}
          \t  C\C: {self.numero}
          \t  Titular: {self.cliente.nome}
        """

class Historico():
    # Lista de transações
    def __init__(self):
        self._transacoes = []

    # Propriedade para receber transações
    @property
    def transacoes(self):
        return self._transacoes

    # Função para adicionar transações
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y (%H:%M:%S)"),
            }
        )

    def gerar_relatorio(self, tipo_transacao = None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual= datetime.now(timezone.utc).date()
        transacoes = []

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d/%m/%Y (%H:%M:%S)").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property    
    def valor(self):
        return self._valor
    
    def  registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def log_transacao(func):
    def envelope(*args, **kwargs):
        # print(Fore.WHITE + 
        #       f"\n{datetime.now().strftime('[%d/%m/%Y %H:%M:%S]')}"
        #       f" {func.__name__.upper()} executado\n"
        # )
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")

        with open(ROOT_PATH / "log.txt", "a", newline='', encoding="utf-8") as arquivo:
            arquivo.write(
            f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. " 
            f"Retornou {resultado}\n"
        )
        print(f"{data_hora}: {func.__name__.upper()}")

        return resultado
    return envelope

def menu():
    menu = f"""
{Fore.CYAN}╔══════════════════════════════════════╗
║         SISTEMA BANCÁRIO             ║
╠══════════════════════════════════════╣
║ [d]  Depositar                       ║
║ [s]  Sacar                           ║
║ [e]  Extrato                         ║
║ [nc] Nova conta                      ║
║ [lc] Listar contas                   ║
║ [nu] Novo usuário                    ║
║ [q]  Sair                            ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
=> """
    return input(menu)
    
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
       print(Fore.YELLOW + "\nCliente não possui conta cadastrada.")
       return
    
    return cliente.contas[0]

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.YELLOW + "\nNenhum cliente encontrado com esse CPF.")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.YELLOW + "\nNenhum cliente encontrado com esse CPF.")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.YELLOW + "\nNenhum cliente encontrado com esse CPF.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print(Fore.CYAN + "\n╔════════════════ EXTRATO ════════════════╗")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += Fore.WHITE + f"""\n
  {transacao['data']}
  {transacao['tipo']} => R$ {transacao['valor']:.2f}
  ────────────────────────────────────────
  """

    if not tem_transacao:
        extrato = Fore.YELLOW + "\n  Não foram realizadas movimentações"

    print(extrato)
    print(f"\n  Saldo Atual:\n\tR$ {conta.saldo:.2f}")
    print(Fore.CYAN + "╚═════════════════════════════════════════╝")

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(Fore.YELLOW + "\nJá existe um cliente cadastrado com esse CPF.")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)
    print(Fore.CYAN + "\n════════════════════════════════════════")
    print(Fore.GREEN + "\tCliente criado com sucesso!")
    print(Fore.CYAN + "════════════════════════════════════════")
@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.YELLOW + "\nNenhum cliente encontrado com esse CPF.")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, limite=500, limite_saques=50)
    contas.append(conta)
    cliente.contas.append(conta)

    print(Fore.CYAN + "\n════════════════════════════════════════")
    print(Fore.GREEN + "\tConta criada com sucesso!")
    print(Fore.CYAN + "════════════════════════════════════════")


def listar_contas(contas):
    for conta in ContaIterador(contas):
        print(Fore.CYAN + "\n╔════════════════ CONTA ═══════════════╗")
        print(Fore.WHITE + textwrap.dedent(str(conta)))
        print(Fore.CYAN + "╚══════════════════════════════════════╝")

def main():
   clientes = []
   contas = []

   while True:
       opcao = menu()

       if opcao == "d":
           depositar(clientes)

       elif opcao == "s":
           sacar(clientes)

       elif opcao == "e":
           exibir_extrato(clientes)

       elif opcao == "nu":
           criar_cliente(clientes)

       elif opcao == "nc":
           numero_conta = len(contas) + 1
           criar_conta(numero_conta, clientes, contas)

       elif opcao == "lc":
           listar_contas(contas)

       elif opcao == "q":
           break

       else:
            print(Fore.RED + "\nInforme uma operação válida.")
main()