import pytest

from ex3_salario.funcionario import Cargo, Funcionario
from ex3_salario.calculadora_salario import CalculadoraSalario


@pytest.fixture
def calc():
    return CalculadoraSalario()


def func(cargo, salario):
    return Funcionario("Maria Souza", "maria@empresa.com", salario, cargo)


@pytest.mark.parametrize(
    "cargo, salario, esperado",
    [
        # DESENVOLVEDOR: 20% se >= 3000, senao 10%
        (Cargo.DESENVOLVEDOR, 3000.00, 2400.00),   # limite
        (Cargo.DESENVOLVEDOR, 5000.00, 4000.00),   # acima
        (Cargo.DESENVOLVEDOR, 2999.99, 2699.99),   # logo abaixo do limite
        (Cargo.DESENVOLVEDOR, 1000.00, 900.00),    # abaixo
        # DBA: 25% se >= 2000, senao 15%
        (Cargo.DBA, 2000.00, 1500.00),
        (Cargo.DBA, 4000.00, 3000.00),
        (Cargo.DBA, 1999.99, 1699.99),
        (Cargo.DBA, 1000.00, 850.00),
        # TESTADOR: 25% se >= 2000, senao 15%
        (Cargo.TESTADOR, 2000.00, 1500.00),
        (Cargo.TESTADOR, 3000.00, 2250.00),
        (Cargo.TESTADOR, 1999.99, 1699.99),
        (Cargo.TESTADOR, 1500.00, 1275.00),
        # GERENTE: 30% se >= 5000, senao 20%
        (Cargo.GERENTE, 5000.00, 3500.00),
        (Cargo.GERENTE, 8000.00, 5600.00),
        (Cargo.GERENTE, 4999.99, 3999.99),
        (Cargo.GERENTE, 2000.00, 1600.00),
    ],
)
def test_salario_liquido(calc, cargo, salario, esperado):
    assert calc.calcular_salario_liquido(func(cargo, salario)) == pytest.approx(esperado)


def test_salario_zero(calc):
    assert calc.calcular_salario_liquido(func(Cargo.DBA, 0)) == 0


def test_salario_negativo_lanca_erro(calc):
    with pytest.raises(ValueError):
        calc.calcular_salario_liquido(func(Cargo.DBA, -100))


def test_salario_nulo_lanca_erro(calc):
    with pytest.raises(ValueError):
        calc.calcular_salario_liquido(func(Cargo.DBA, None))


def test_cargo_invalido_lanca_erro(calc):
    with pytest.raises(ValueError):
        calc.calcular_salario_liquido(func("ESTAGIARIO", 1000))
