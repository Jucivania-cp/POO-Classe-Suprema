from abc import ABC, abstractmethod
from datetime import datetime

class Publicacao(ABC):
    def __init__ (self, titulo, autor, ano, genero, paginas):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.paginas = paginas
        self._status = "NÃO LIDO"
        self._avaliacao = 0.0
        self.data_inclusao
        self.data_fim
        self.anotacoes = []

    @property
    def titulo(self):
        return self._titulo
    
    @titulo.setter
    def titulo(self, valor):
        if not valor or not valor.strip():
            raise ValueError ("O título não pode ser vazio")
        self._titulo = valor

    @property
    def ano(self):
        return self._ano
    
    @ano.setter
    def ano (self, valor):
        if valor < 1500:
            raise ValueError ("O ano de publicação deve ser maior ou igual a 1500")
        self._ano = valor

    @property
    def avaliacao(self):
        return self._avaliacao
    
    @avaliacao.setter
    def avaliacao (self, valor):
        if self._status != "LIDO":
            raise ValueError ("Avaliação só pode ser feita após o status ser 'LIDO'")
        if not (0 <= valor <= 10):
            raise ValueError ("A nota deve estar entre 0 e 10")
        self._avaliacao = valor

    @property
    def status(self):
        return self._status


class Livro(Publicacao):
    def __init__(self, titulo, autor, ano, genero, paginas,isbn):
        super.__init__(self, titulo, autor, ano, genero, paginas)
        self.isbn = isbn

    def __str__(self):
        return f"[LIVRO] {super().__str__()} | ISBN: {self.isbn}"
    
class Revista(Publicacao):
    def __init__(self, titulo, autor, ano, genero, paginas,edicao):
        super.__init__(self, titulo, autor, ano, genero, paginas)
        self.edicao = edicao

    def __str__(self):
        return f"[REVISTA] {super().__str__()} | EDIÇÃO: {self.edicao}"