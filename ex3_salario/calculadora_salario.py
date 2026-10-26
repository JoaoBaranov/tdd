from ex3_salario.funcionario import Cargo, Funcionario

# cargo -> (limite, desconto se salario >= limite, desconto se salario < limite)
REGRAS = {
    Cargo.DESENVOLVEDOR: (3000.00, 0.20, 0.10),
    Cargo.DBA:           (2000.00, 0.25, 0.15),
    Cargo.TESTADOR:      (2000.00, 0.25, 0.15),
    Cargo.GERENTE:       (5000.00, 0.30, 0.20),
}


class CalculadoraSalario:
    def calcular_salario_liquido(self, f: Funcionario) -> float:
        if f.cargo not in REGRAS:
            raise ValueError("Cargo invalido")
        if f.salario_base is None or f.salario_base < 0:
            raise ValueError("Salario base invalido")

        limite, desconto_alto, desconto_baixo = REGRAS[f.cargo]
        desconto = desconto_alto if f.salario_base >= limite else desconto_baixo
        return round(f.salario_base * (1 - desconto), 2)
