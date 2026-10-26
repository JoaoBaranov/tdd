class Email:
    def __init__(self, id: int, name: str):
        self.id = id
        # o "name" do Email guarda o endereco completo (ex: joao@gmail.com)
        self.name = name


class Person:
    def __init__(self, id: int, name: str, age: int, emails: list = None):
        self.id = id
        self.name = name
        self.age = age
        # relacao 1 -> 1..* (uma pessoa possui um ou mais emails)
        self.emails = emails if emails is not None else []
