from src.models.publicacao import Publicacao
from src.models.anotacao import Anotacao
from datetime import datetime

class Livro(Publicacao):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int, isbn: str | None = None) -> None:
        super().__init__(titulo, autor, ano, genero, paginas)
        self._isbn = isbn

    # ---------------- PROPERTIES ----------------
    @property
    def isbn(self) -> str | None:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str | None) -> None:
        if valor is not None and not valor.isdigit():
            raise ValueError("ISBN deve conter apenas números.")
        self._isbn = valor

    # ---------------- MÉTODOS ----------------
    def __str__(self) -> str:
        base = super().__str__()
        return base + (f" | ISBN: {self.isbn}" if self.isbn else "")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["isbn"] = self.isbn
        return d

    @staticmethod
    def from_dict(d: dict) -> "Livro":
        obj = Livro(
            d["titulo"],
            d["autor"],
            d["ano"],
            d["genero"],
            d["paginas"],
            d.get("isbn")
        )
        # Restaurar atributos herdados
        obj.status = d.get("status", "NÃO LIDO")
        obj.avaliacao = d.get("avaliacao")
        obj.anotacoes = [Anotacao.from_dict(a) for a in d.get("anotacoes", [])]

        obj.data_inclusao = datetime.fromisoformat(d["data_inclusao"]) if d.get("data_inclusao") else datetime.now()
        obj.data_inicio = datetime.fromisoformat(d["data_inicio"]) if d.get("data_inicio") else None
        obj.data_fim = datetime.fromisoformat(d["data_fim"]) if d.get("data_fim") else None
        return obj
