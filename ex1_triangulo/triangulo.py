from enum import Enum


class TipoTriangulo(Enum):
    EQUILATERO = "equilatero"
    ISOSCELES = "isosceles"
    ESCALENO = "escaleno"
    INVALIDO = "invalido"


class Triangulo:
    """Recebe os tres lados e diz que tipo de triangulo eles formam."""

    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c

    def _eh_valido(self) -> bool:
        # nenhum lado pode ser zero ou negativo
        if self.a <= 0 or self.b <= 0 or self.c <= 0:
            return False
        # a soma de dois lados tem que ser MAIOR que o terceiro
        return (
            self.a + self.b > self.c
            and self.a + self.c > self.b
            and self.b + self.c > self.a
        )

    def classificar(self) -> TipoTriangulo:
        if not self._eh_valido():
            return TipoTriangulo.INVALIDO
        if self.a == self.b == self.c:
            return TipoTriangulo.EQUILATERO
        if self.a == self.b or self.a == self.c or self.b == self.c:
            return TipoTriangulo.ISOSCELES
        return TipoTriangulo.ESCALENO
