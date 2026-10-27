# Atividade de TDD - Lucas Nadalete

Repositório com a resolução dos 3 exercícios de JUnit e TDD. Fiz em Python com pytest porque é a linguagem que eu tenho mais costume, e o pytest-cov mostra a cobertura de um jeito fácil.

URL do repositório: https://github.com/JoaoBaranov/tdd

## Estrutura

```
tdd/
├── ex1_triangulo/
│   └── triangulo.py
├── ex2_pessoa/
│   ├── models.py
│   └── person_dao.py
├── ex3_salario/
│   ├── funcionario.py
│   └── calculadora_salario.py
├── tests/
│   ├── test_triangulo.py
│   ├── test_person_dao.py
│   └── test_calculadora_salario.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Como rodar

Precisa ter o Python 3.9 ou mais novo. Como Python não tem build igual o Maven, o "build" é só criar o ambiente virtual e instalar as dependências.

```bash
git clone https://github.com/JoaoBaranov/tdd.git
cd tdd

python -m venv .venv
source .venv/bin/activate      # no Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Rodar os testes:

```bash
python -m pytest -v
```

Rodar com cobertura:

```bash
python -m pytest --cov=ex1_triangulo --cov=ex2_pessoa --cov=ex3_salario --cov-report=term-missing
```

Também dá pra gerar o relatório em HTML trocando o final por `--cov-report=html` (abre em `htmlcov/index.html`).

## Sobre o TDD

Em cada exercício a ideia foi escrever o teste primeiro, ver falhar, fazer o código mínimo pra passar e depois melhorar (red, green, refactor). Os commits ficaram um por exercício.

## Exercício 1 - Triângulo

A classe `Triangulo` recebe os três lados e o método `classificar()` devolve se é equilátero, isósceles, escaleno ou inválido. Pra ser válido, nenhum lado pode ser zero ou negativo e a soma de dois lados tem que ser maior que o terceiro (se for igual, não forma triângulo).

Casos de teste (`tests/test_triangulo.py`):

| Item | Situação | Entradas | Resultado |
|------|----------|----------|-----------|
| 2.1 | Escaleno | (3,4,5) | ESCALENO |
| 2.2 | Isósceles | (5,5,8) | ISOSCELES |
| 2.3 | Equilátero | (4,4,4) | EQUILATERO |
| 2.4 | Isósceles, permutações | (3,3,4) (3,4,3) (4,3,3) | ISOSCELES |
| 2.5 | Um valor zero | (0,4,5) (4,0,5) (4,5,0) | INVALIDO |
| 2.6 | Um valor negativo | (-1,4,4) (4,-1,4) (4,4,-1) | INVALIDO |
| 2.7 e 2.8 | Soma igual ao terceiro lado | 6 permutações de (1,2,3) | INVALIDO |
| 2.9 e 2.10 | Soma menor que o terceiro lado | 6 permutações de (1,2,4) | INVALIDO |
| 2.11 | Três zeros | (0,0,0) | INVALIDO |

Cobertura:

```
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
ex1_triangulo/__init__.py        0      0   100%
ex1_triangulo/triangulo.py      23      0   100%
----------------------------------------------------------
TOTAL                           23      0   100%
25 passed
```

## Exercício 2 - Person, Email e PersonDAO

Segui o diagrama: `Person` (id, name, age) tem uma lista de `Email` (id, name), e o `PersonDAO` tem `save()` e `is_valid_to_include()` (usei snake_case porque é o padrão do Python).

O `is_valid_to_include()` devolve uma lista com os erros. Se a lista vem vazia, a pessoa é válida. As validações são:

- nome com pelo menos 2 partes e só letras
- idade entre 1 e 200
- pelo menos um email
- email no formato `x@y.z`, com pelo menos 1 caractere em cada parte (usei uma regex)

O `save()` só guarda a pessoa se não tiver erro, senão lança `ValueError`. Os dados ficam numa lista em memória porque o exercício não pede banco.

Nos testes tentei cobrir os valores de fronteira da idade (0, 1, 2, 199, 200, 201), vários emails inválidos, pessoa sem email e um caso com todos os erros juntos.

Cobertura:

```
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
ex2_pessoa/__init__.py         0      0   100%
ex2_pessoa/models.py          10      0   100%
ex2_pessoa/person_dao.py      33      0   100%
--------------------------------------------------------
TOTAL                         43      0   100%
33 passed
```

## Exercício 3 - Calculadora de salário

Tem a classe `Funcionario` (nome, email, salário base e cargo), o enum `Cargo` e a `CalculadoraSalario`, com o método `calcular_salario_liquido()`. As regras de desconto ficam num dicionário (cargo, limite, desconto maior, desconto menor), assim não precisa de vários if/elif.

Desconto (se o salário é maior ou igual ao limite / se é menor):

- Desenvolvedor: limite 3.000, 20% / 10%
- DBA: limite 2.000, 25% / 15%
- Testador: limite 2.000, 25% / 15%
- Gerente: limite 5.000, 30% / 20%

Pra cada cargo testei o valor exatamente no limite, um acima e um logo abaixo (tipo 2999,99). Também testei salário zero, negativo, nulo e cargo inválido.

Cobertura:

```
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
ex3_salario/__init__.py                  0      0   100%
ex3_salario/calculadora_salario.py      11      0   100%
ex3_salario/funcionario.py              12      0   100%
------------------------------------------------------------------
TOTAL                                   23      0   100%
20 passed
```

## Resultado geral

Rodando tudo junto: 78 testes passando e 100% de cobertura nos três exercícios.

## Observações

- Testar os valores do limite (3000, 2000, 5000, idade 1 e 200) é importante porque é ali que costuma dar erro, tipo usar `>=` no lugar de `>`.
- 100% de cobertura só quer dizer que todas as linhas rodaram nos testes, não que não tem bug.
- Na hora de subir pro GitHub o terminal não aceitou a senha da conta, tive que usar um token de acesso pessoal.
- Em Java ficaria parecido, trocando pytest por JUnit 5 e pytest-cov por JaCoCo.
