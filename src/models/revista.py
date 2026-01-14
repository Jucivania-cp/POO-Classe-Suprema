from src.models.publicacao import Publicacao

class Revista(Publicacao):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int,
                 edicao: int, status: str = "NAO_LIDO", avaliacao: int = None):
        super().__init__(titulo, autor, ano, genero, paginas, status, avaliacao)
        self.edicao = edicao

    @property
    def edicao(self):
        return self.__edicao

    @edicao.setter
    def edicao(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Edição deve ser um número inteiro positivo.")
        self.__edicao = value

    def __str__(self):
        return f"{super().__str__()} | Edição: {self.edicao}"

    def __repr__(self):
        return f"<Revista titulo='{self.titulo}', autor='{self.autor}', ano={self.ano}, edicao={self.edicao}>"

    def tipo(self):
        return "Revista"
