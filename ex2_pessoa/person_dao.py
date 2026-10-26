import re

from ex2_pessoa.models import Person

ERRO_NOME_PARTES = "O nome deve ter ao menos 2 partes"
ERRO_NOME_LETRAS = "O nome deve ser composto apenas por letras"
ERRO_IDADE = "A idade deve estar no intervalo [1, 200]"
ERRO_SEM_EMAIL = "A pessoa deve ter ao menos um email"
ERRO_EMAIL_FORMATO = "Email invalido (formato esperado: x@y.z): "

# parte@dominio.extensao -> cada parte com pelo menos 1 caractere
REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")


class PersonDAO:
    def __init__(self):
        self._pessoas = []  # "banco de dados" em memoria

    def is_valid_to_include(self, p: Person) -> list:
        """Devolve a lista de erros. Lista vazia = pessoa valida."""
        erros = []

        # --- nome ---
        partes = p.name.split() if isinstance(p.name, str) else []
        if len(partes) < 2:
            erros.append(ERRO_NOME_PARTES)
        if any(not parte.isalpha() for parte in partes):
            erros.append(ERRO_NOME_LETRAS)

        # --- idade ---
        if not isinstance(p.age, int) or p.age < 1 or p.age > 200:
            erros.append(ERRO_IDADE)

        # --- emails ---
        if not p.emails:
            erros.append(ERRO_SEM_EMAIL)
        else:
            for email in p.emails:
                if not REGEX_EMAIL.match(email.name or ""):
                    erros.append(ERRO_EMAIL_FORMATO + str(email.name))

        return erros

    def save(self, p: Person) -> None:
        erros = self.is_valid_to_include(p)
        if erros:
            raise ValueError(erros)
        self._pessoas.append(p)

    def listar(self) -> list:
        return list(self._pessoas)
