from abc import ABC, abstractmethod

# Classe Cliente: representa um cliente genérico com endereço e contas.
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []  # Lista para armazenar contas do cliente.

    # Método para realizar uma transação (depósito ou saque) em uma conta.
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)  # Transação é registrada na conta.
        print("Transação realizada com sucesso!")

    # Método para adicionar uma conta ao cliente.
    def adicionar_conta(self, conta):
        self._contas.append(conta)  # Conta adicionada à lista do cliente.
        print(f"Conta {conta._numero} adicionada ao cliente {self._nome}.")

    def __str__(self):
        return f"Nome: {self._nome}, Cpf: {self._cpf}, Data de Nascimento: {self._data_nascimento}, Endereço: {self._endereco}"

# Classe Pessoa_fisica: herda de Cliente e adiciona atributos como CPF e nome.
class Pessoa_fisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

# Classe Conta_corrente: define o limite da conta e limite de saques.
class Conta_corrente:
    def __init__(self, limite=500, limite_de_saque=0):
        self._limite = limite  # Limite da conta.
        self._limite_de_saque = limite_de_saque  # Contador de saques.

# Classe Conta: herda de Conta_corrente e adiciona atributos como saldo e cliente.
class Conta(Conta_corrente):
    def __init__(self, saldo, numero, agencia, cliente, historico, limite, limite_de_saque):
        super().__init__(limite, limite_de_saque)
        self._saldo = float(saldo)  # Saldo inicial da conta.
        self._numero = numero  # Número da conta.
        self._agencia = agencia  # Agência da conta.
        self._cliente = cliente  # Nome do cliente.
        self._historico = historico  # Historico de transações.

    # Método para consultar o saldo da conta.
    def saldo(self):
        print("Saldo:", self._saldo)

    # Método para criar uma nova conta.
    def nova_conta(self, cliente, numero):
        self._cliente = cliente
        self._numero = numero
        print("Conta nova criada com sucesso!")
        return Conta

    # Método privado para realizar o saque internamente (não diretamente acessado pelo usuário).
    def _sacar(self, valor):
        if valor <= self._saldo and valor <= self._limite and self._limite_de_saque < 3:
            self._saldo -= valor  # Deduz o valor do saldo.
            self._limite_de_saque += 1  # Incrementa o contador de saques.
            return True
        else:
            return False

    # Método privado para realizar o depósito internamente (não diretamente acessado pelo usuário).
    def _depositar(self, valor):
        self._saldo += valor  # Adiciona o valor ao saldo.
        return True  # Retorna True indicando sucesso.

    def __str__(self):
        return f"Número: {self._numero}, Agência: {self._agencia}, Saldo: {self._saldo}, Cliente: {self._cliente}"

# Classe abstrata Transacao: define o contrato para qualquer transação (depósito ou saque).
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Classe Deposito: implementa uma transação de depósito.
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = float(valor)  # Valor do depósito.

    # Método que registra o depósito na conta.
    def registrar(self, conta):
        if conta._depositar(self._valor):  # Chama o método privado _depositar da conta.
            print(f"Depósito de {self._valor} registrado com sucesso na conta {conta._numero}.")

# Classe Saque: implementa uma transação de saque.
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = float(valor)  # Valor do saque.

    # Método que registra o saque na conta.
    def registrar(self, conta):
        if conta._sacar(self._valor):  # Chama o método privado _sacar da conta.
            print(f"Saque de {self._valor} registrado com sucesso na conta {conta._numero}.")
        else:
            print("Saque não realizado. Verifique saldo ou limite de saques.")

# Classe Historico: armazena e executa transações.
class Historico:
    def adicionar_transacao(self, transacao, conta):
        transacao.registrar(conta)  # Adiciona a transação ao histórico da conta.

# Exemplo de uso:

# Criando clientes
print("=========== CLIENTES ===========")
cliente01 = Pessoa_fisica("08888888888", "Endrew", "16/07/1999", "Rua dos Bobos, Número 93")
cliente02 = Pessoa_fisica("08888888889", "Burgue", "16/05/1999", "Rua dos Tolos, Número 95")
print(f"Cliente 1:\n{cliente01}\n")
print(f"Cliente 2:\n{cliente02}\n")

# Criando contas
print("=========== CONTAS ===========")
conta01 = Conta("600", "1", "001", cliente01._nome, "Histórico", 500, 0)
conta02 = Conta("600", "2", "001", cliente02._nome, "Histórico", 500, 0)
print(f"Conta 1:\n{conta01}\n")
print(f"Conta 2:\n{conta02}\n")

# Adicionando contas aos clientes
print("=========== ADICIONANDO CONTAS AOS CLIENTES ===========")
cliente01.adicionar_conta(conta01)
cliente02.adicionar_conta(conta02)

print("\n")
# Criando novas contas
print("=========== CRIANDO NOVAS CONTAS ===========")
conta01.nova_conta(cliente01._nome, "3")
conta02.nova_conta(cliente02._nome, "4")

# Criando transações
deposito = Deposito("500")
saque = Saque("600")

print("\n")
# Histórico de transações
print("=========== HISTÓRICO DE TRANSAÇÕES ===========")
historico = Historico()
historico.adicionar_transacao(deposito, conta01)
historico.adicionar_transacao(saque, conta02)

print("\n")
# Verificando saldo após transações
print("=========== SALDO FINAL ===========")
conta01.saldo()
conta02.saldo()
