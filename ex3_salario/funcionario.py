from enum import Enum


class Cargo(Enum):
    DESENVOLVEDOR = "DESENVOLVEDOR"
    DBA = "DBA"
    TESTADOR = "TESTADOR"
    GERENTE = "GERENTE"


class Funcionario:
    def __init__(self, nome: str, email: str, salario_base: float, cargo: Cargo):
        self.nome = nome
        self.email = email
        self.salario_base = salario_base
        self.cargo = cargo
