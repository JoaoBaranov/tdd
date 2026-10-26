import pytest

from ex1_triangulo.triangulo import Triangulo, TipoTriangulo


def tipo(a, b, c):
    return Triangulo(a, b, c).classificar()


# 2.1 escaleno valido
def test_escaleno_valido():
    assert tipo(3, 4, 5) == TipoTriangulo.ESCALENO


# 2.2 isosceles valido
def test_isosceles_valido():
    assert tipo(5, 5, 8) == TipoTriangulo.ISOSCELES


# 2.3 equilatero valido
def test_equilatero_valido():
    assert tipo(4, 4, 4) == TipoTriangulo.EQUILATERO


# 2.4 isosceles: 3 permutacoes dos mesmos valores
@pytest.mark.parametrize("a, b, c", [(3, 3, 4), (3, 4, 3), (4, 3, 3)])
def test_isosceles_permutacoes(a, b, c):
    assert tipo(a, b, c) == TipoTriangulo.ISOSCELES


# 2.5 um valor zero (testando o zero em cada posicao)
@pytest.mark.parametrize("a, b, c", [(0, 4, 5), (4, 0, 5), (4, 5, 0)])
def test_um_lado_zero(a, b, c):
    assert tipo(a, b, c) == TipoTriangulo.INVALIDO


# 2.6 um valor negativo (em cada posicao)
@pytest.mark.parametrize("a, b, c", [(-1, 4, 4), (4, -1, 4), (4, 4, -1)])
def test_um_lado_negativo(a, b, c):
    assert tipo(a, b, c) == TipoTriangulo.INVALIDO


# 2.7 e 2.8 soma de 2 lados IGUAL ao terceiro (todas as 6 permutacoes de 1,2,3)
@pytest.mark.parametrize(
    "a, b, c",
    [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)],
)
def test_soma_dois_lados_igual_ao_terceiro(a, b, c):
    assert tipo(a, b, c) == TipoTriangulo.INVALIDO


# 2.9 e 2.10 soma de 2 lados MENOR que o terceiro (todas as 6 permutacoes de 1,2,4)
@pytest.mark.parametrize(
    "a, b, c",
    [(1, 2, 4), (1, 4, 2), (2, 1, 4), (2, 4, 1), (4, 1, 2), (4, 2, 1)],
)
def test_soma_dois_lados_menor_que_o_terceiro(a, b, c):
    assert tipo(a, b, c) == TipoTriangulo.INVALIDO


# 2.11 os tres valores zero
def test_tres_lados_zero():
    assert tipo(0, 0, 0) == TipoTriangulo.INVALIDO
