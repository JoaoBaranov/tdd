# Atividade de TDD – Triângulo, Pessoa/Email e Calculadora de Salário

Oi! Esse repositório tem a resolução dos 3 exercícios de **JUnit e TDD** da disciplina de teste de software.
Eu escolhi fazer em **Python com pytest**, porque já tenho mais costume com a linguagem e o `pytest-cov`
deixa muito fácil mostrar a cobertura de código.

> **URL do repositório:** `https://github.com/SEU-USUARIO/tdd-projeto` *(troquei pelo meu link na hora de entregar)*

---

## Estrutura do projeto

```
tdd-projeto/
├── ex1_triangulo/
│   └── triangulo.py              # classe Triangulo + enum TipoTriangulo
├── ex2_pessoa/
│   ├── models.py                 # classes Person e Email
│   └── person_dao.py             # PersonDAO com is_valid_to_include() e save()
├── ex3_salario/
│   ├── funcionario.py            # classe Funcionario + enum Cargo
│   └── calculadora_salario.py    # CalculadoraSalario
├── tests/
│   ├── test_triangulo.py
│   ├── test_person_dao.py
│   └── test_calculadora_salario.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Como fazer o build e rodar os testes

Precisa do **Python 3.9+** instalado. Python não tem "build" de verdade como o Maven do Java,
então o "build" aqui é só criar o ambiente virtual e instalar as dependências.

```bash
# 1. clonar o repositório
git clone https://github.com/SEU-USUARIO/tdd-projeto.git
cd tdd-projeto

# 2. criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# 3. instalar as dependências (pytest e pytest-cov)
pip install -r requirements.txt

# 4. rodar todos os testes
python -m pytest -v

# 5. rodar com cobertura de código
python -m pytest --cov=ex1_triangulo --cov=ex2_pessoa --cov=ex3_salario --cov-report=term-missing

# (opcional) gerar o relatório em HTML, abre em htmlcov/index.html
python -m pytest --cov=ex1_triangulo --cov=ex2_pessoa --cov=ex3_salario --cov-report=html
```

Para rodar só um exercício:

```bash
python -m pytest tests/test_triangulo.py --cov=ex1_triangulo
python -m pytest tests/test_person_dao.py --cov=ex2_pessoa
python -m pytest tests/test_calculadora_salario.py --cov=ex3_salario
```

---

## Como eu apliquei o TDD

Em todos os exercícios eu tentei seguir o ciclo **Red → Green → Refactor**:

1. **Red:** escrevo o teste primeiro e vejo ele falhar;
2. **Green:** escrevo o mínimo de código para ele passar;
3. **Refactor:** limpo o código sem quebrar os testes.

Fui fazendo um commit por etapa, tipo `test: escaleno valido (red)` e depois `feat: classifica escaleno (green)`,
então dá para ver o passo a passo no histórico do Git.

---

## Exercício 1 – Triângulo

**Esqueleto da classe** (item 1): a classe `Triangulo` recebe os 3 lados no construtor e tem o método
`classificar()`, que devolve um `TipoTriangulo` (`EQUILATERO`, `ISOSCELES`, `ESCALENO` ou `INVALIDO`).

Regra de validade: todos os lados > 0 **e** a soma de quaisquer dois lados **maior** que o terceiro
(se for igual, também é inválido, porque vira uma linha reta).

**Casos de teste** (`tests/test_triangulo.py`):

| Item | Situação | Entradas testadas | Esperado |
|------|----------|-------------------|----------|
| 2.1 | Escaleno válido | (3, 4, 5) | ESCALENO |
| 2.2 | Isósceles válido | (5, 5, 8) | ISOSCELES |
| 2.3 | Equilátero válido | (4, 4, 4) | EQUILATERO |
| 2.4 | Isósceles – permutações | (3,3,4), (3,4,3), (4,3,3) | ISOSCELES |
| 2.5 | Um valor zero | (0,4,5), (4,0,5), (4,5,0) | INVALIDO |
| 2.6 | Um valor negativo | (-1,4,4), (4,-1,4), (4,4,-1) | INVALIDO |
| 2.7 / 2.8 | Soma de 2 lados **igual** ao terceiro | as 6 permutações de (1,2,3) | INVALIDO |
| 2.9 / 2.10 | Soma de 2 lados **menor** que o terceiro | as 6 permutações de (1,2,4) | INVALIDO |
| 2.11 | Três valores zero | (0, 0, 0) | INVALIDO |

Usei `@pytest.mark.parametrize` nas permutações para não ficar copiando e colando o mesmo teste várias vezes.

### Evidência de cobertura – Exercício 1

```
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
ex1_triangulo/__init__.py        0      0   100%
ex1_triangulo/triangulo.py      23      0   100%
----------------------------------------------------------
TOTAL                           23      0   100%
25 passed
```

---

## Exercício 2 – Person, Email e PersonDAO

Implementei o diagrama de classes do enunciado: `Person` (id, name, age) se relaciona com `1..*` objetos `Email`
(id, name). O `PersonDAO` tem o `save()` e o `is_valid_to_include()`.
*(No Python o padrão é snake_case, então o `isValidToInclude` do diagrama virou `is_valid_to_include`.)*

O método retorna uma **lista de erros** (lista vazia = pessoa válida). As regras validadas são:

- **Nome:** pelo menos 2 partes e só letras (aceita acento, tipo "José da Conceição");
- **Idade:** entre 1 e 200 (testei os valores de fronteira: 0, 1, 2, 199, 200, 201);
- **Emails:** a pessoa precisa ter pelo menos um;
- **Formato do email:** `_____@____._____`, cada parte com pelo menos 1 caractere. Usei uma regex para isso.

O `save()` só guarda a pessoa se não tiver erros; se tiver, lança `ValueError` com a lista de erros.
Como não tem banco de dados de verdade no exercício, os dados ficam numa lista em memória.

**Principais testes** (`tests/test_person_dao.py`): pessoa válida, nome com 1 parte, nome vazio/nulo, nome com número
ou símbolo, idades limite, pessoa sem email, 8 formatos de email inválidos, 3 válidos, vários emails com um ruim,
todos os erros ao mesmo tempo e o `save()` com pessoa válida e inválida.

### Evidência de cobertura – Exercício 2

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

---

## Exercício 3 – Calculadora de salário

Classes: `Funcionario` (nome, email, salário base, cargo), enum `Cargo` e `CalculadoraSalario`,
que tem o método `calcular_salario_liquido()`.

Em vez de fazer um monte de `if/elif` para cada cargo, guardei as regras em um dicionário
(`cargo -> (limite, desconto alto, desconto baixo)`). Isso eu só percebi na fase de **refactor**, depois que os testes
já estavam passando.

| Cargo | Limite | Desconto se salário ≥ limite | Desconto se salário < limite |
|-------|--------|------------------------------|------------------------------|
| DESENVOLVEDOR | R$ 3.000,00 | 20% | 10% |
| DBA | R$ 2.000,00 | 25% | 15% |
| TESTADOR | R$ 2.000,00 | 25% | 15% |
| GERENTE | R$ 5.000,00 | 30% | 20% |

Para cada cargo testei três situações: exatamente **no limite**, **acima** e **logo abaixo** (ex.: 2999,99).
Também testei salário zero, salário negativo, salário nulo e cargo inválido (esses lançam `ValueError`).

### Evidência de cobertura – Exercício 3

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

---

## Resultado geral

Rodando tudo junto (`python -m pytest`): **78 testes passando** e **100% de cobertura** nos três exercícios.

---

## O que eu aprendi / dificuldades

- No começo era difícil resistir à vontade de escrever o código antes do teste. Mas quando fiz do jeito certo,
  percebi que o teste me obrigava a pensar primeiro nas regras do problema.
- No triângulo, o caso "soma igual ao terceiro lado" é o mais fácil de errar: se usar `>=` em vez de `>`
  o teste do item 2.7 falha na hora. Foi legal ver o teste pegando um bug de verdade.
- Valor limite (3000, 2000, 5000, idade 1 e 200) é onde os bugs aparecem, então testei sempre nas fronteiras.
- Cobertura de 100% não quer dizer que não tem bug, só que todas as linhas foram executadas por algum teste.
  Por isso me preocupei mais em ter bons casos de teste do que só em bater o número.
- Se fosse em Java, as classes seriam praticamente as mesmas, trocando pytest por JUnit 5 e o `pytest-cov` pelo JaCoCo.
