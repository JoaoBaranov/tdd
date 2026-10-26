import pytest

from ex2_pessoa.models import Person, Email
from ex2_pessoa.person_dao import (
    PersonDAO,
    ERRO_NOME_PARTES,
    ERRO_NOME_LETRAS,
    ERRO_IDADE,
    ERRO_SEM_EMAIL,
    ERRO_EMAIL_FORMATO,
)


@pytest.fixture
def dao():
    return PersonDAO()


def pessoa_valida(**kwargs):
    dados = dict(id=1, name="Joao Silva", age=30, emails=[Email(1, "joao@gmail.com")])
    dados.update(kwargs)
    return Person(**dados)


# ---------- pessoa valida ----------
def test_pessoa_valida_nao_tem_erros(dao):
    assert dao.is_valid_to_include(pessoa_valida()) == []


# ---------- nome ----------
def test_nome_com_uma_parte(dao):
    assert dao.is_valid_to_include(pessoa_valida(name="Joao")) == [ERRO_NOME_PARTES]


def test_nome_vazio(dao):
    assert ERRO_NOME_PARTES in dao.is_valid_to_include(pessoa_valida(name=""))


def test_nome_nulo(dao):
    assert ERRO_NOME_PARTES in dao.is_valid_to_include(pessoa_valida(name=None))


def test_nome_com_numero(dao):
    assert dao.is_valid_to_include(pessoa_valida(name="Joao Silva2")) == [ERRO_NOME_LETRAS]


def test_nome_com_simbolo(dao):
    assert dao.is_valid_to_include(pessoa_valida(name="Joao @Silva")) == [ERRO_NOME_LETRAS]


def test_nome_com_acento_e_tres_partes_eh_valido(dao):
    assert dao.is_valid_to_include(pessoa_valida(name="José da Conceição")) == []


# ---------- idade (valores limite) ----------
@pytest.mark.parametrize("idade", [1, 2, 199, 200])
def test_idade_valida(dao, idade):
    assert dao.is_valid_to_include(pessoa_valida(age=idade)) == []


@pytest.mark.parametrize("idade", [0, -1, 201, 1000])
def test_idade_invalida(dao, idade):
    assert dao.is_valid_to_include(pessoa_valida(age=idade)) == [ERRO_IDADE]


def test_idade_nao_inteira(dao):
    assert dao.is_valid_to_include(pessoa_valida(age="trinta")) == [ERRO_IDADE]


# ---------- emails ----------
def test_pessoa_sem_email(dao):
    assert dao.is_valid_to_include(pessoa_valida(emails=[])) == [ERRO_SEM_EMAIL]


def test_pessoa_com_emails_none(dao):
    assert dao.is_valid_to_include(pessoa_valida(emails=None)) == [ERRO_SEM_EMAIL]


@pytest.mark.parametrize(
    "endereco",
    [
        "joaogmail.com",   # sem @
        "joao@gmail",      # sem ponto/extensao
        "@gmail.com",      # sem parte local
        "joao@.com",       # dominio vazio
        "joao@gmail.",     # extensao vazia
        "joao@@gmail.com", # dois @
        "",                # vazio
        None,              # nulo
    ],
)
def test_email_com_formato_invalido(dao, endereco):
    p = pessoa_valida(emails=[Email(1, endereco)])
    assert dao.is_valid_to_include(p) == [ERRO_EMAIL_FORMATO + str(endereco)]


@pytest.mark.parametrize("endereco", ["a@b.c", "joao.silva@gmail.com", "x@empresa.com.br"])
def test_email_com_formato_valido(dao, endereco):
    p = pessoa_valida(emails=[Email(1, endereco)])
    assert dao.is_valid_to_include(p) == []


def test_varios_emails_um_invalido(dao):
    p = pessoa_valida(emails=[Email(1, "ok@ok.com"), Email(2, "ruim")])
    assert dao.is_valid_to_include(p) == [ERRO_EMAIL_FORMATO + "ruim"]


# ---------- varios erros juntos ----------
def test_todos_os_erros_juntos(dao):
    p = Person(1, "Joao", 0, [])
    erros = dao.is_valid_to_include(p)
    assert erros == [ERRO_NOME_PARTES, ERRO_IDADE, ERRO_SEM_EMAIL]


# ---------- save ----------
def test_save_pessoa_valida(dao):
    p = pessoa_valida()
    dao.save(p)
    assert dao.listar() == [p]


def test_save_pessoa_invalida_lanca_erro_e_nao_salva(dao):
    with pytest.raises(ValueError):
        dao.save(pessoa_valida(age=0))
    assert dao.listar() == []
