from publicacao import Publicacao

class Livro(Publicacao):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int,
                 isbn: str, status: str = "NÃO LIDO", avaliacao: int = None):
        super().__init__(titulo, autor, ano, genero, paginas, status, avaliacao)
        self.isbn = isbn

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, value: str):
        if not value or not value.strip():
            raise ValueError("ISBN não pode ser vazio.")
        if len(value.strip()) not in (10, 13):
            raise ValueError("ISBN deve ter 10 ou 13 caracteres.")
        self.__isbn = value.strip()

    def __str__(self):
        return f"{super().__str__()} | ISBN: {self.isbn}"

    def __repr__(self):
        return f"<Livro titulo='{self.titulo}', autor='{self.autor}', ano={self.ano}, isbn='{self.isbn}'>"

    def tipo(self):
        return "Livro"

    def to_dict(self):
        data = super().to_dict()
        data["isbn"] = self.isbn
        return data

    @classmethod
    def from_dict(cls, dados):
        return cls(
            titulo=dados["titulo"],
            autor=dados["autor"],
            ano=dados["ano"],
            genero=dados["genero"],
            paginas=dados["paginas"],
            isbn=dados["isbn"],
            status=dados.get("status", "NAO_LIDO"),
            avaliacao=dados.get("avaliacao"),
        )

