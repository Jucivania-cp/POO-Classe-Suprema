from publicacao import Publicacao

class Revista(Publicacao):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int,
                 edicao: int, status: str = "NÃO LIDO", avaliacao: int = None):
        super().__init__(titulo, autor, ano, genero, paginas, status, avaliacao)
        self.edicao = edicao

    @property
    def edicao(self) -> int:
        return self.__edicao

    @edicao.setter
    def edicao(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Edição deve ser um número inteiro positivo.")
        self.__edicao = value

    def __str__(self):
        return f"{super().__str__()} | Edição: {self.edicao}"

    def __repr__(self):
        return f"<Revista titulo='{self.titulo}', autor='{self.autor}', ano={self.ano}, edicao={self.edicao}>"

    def tipo(self):
        return "Revista"

    def to_dict(self):
        data = super().to_dict()
        data["edicao"] = self.edicao
        return data

    @classmethod
    def from_dict(cls, dados):
        return cls(
            titulo=dados["titulo"],
            autor=dados["autor"],
            ano=dados["ano"],
            genero=dados["genero"],
            paginas=dados["paginas"],
            edicao=dados["edicao"],
            status=dados.get("status", "NAO_LIDO"),
            avaliacao=dados.get("avaliacao"),
        )

