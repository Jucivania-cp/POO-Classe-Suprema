from src.models.publicacao import Publicacao
from src.models.anotacao import Anotacao
from datetime import datetime

class Revista(Publicacao):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int, edicao: int | None = None) -> None:
        super().__init__(titulo, autor, ano, genero, paginas)
        self._edicao = edicao

    # ---------------- PROPERTIES ----------------
    @property
    def edicao(self) -> int | None:
        return self._edicao

    @edicao.setter
    def edicao(self, valor: int | None) -> None:
        if valor is not None and valor <= 0:
            raise ValueError("Edição deve ser positiva.")
        self._edicao = valor

    # ---------------- MÉTODOS ----------------
    def __str__(self) -> str:
        base = super().__str__()
        return base + (f" | Edição: {self.edicao}" if self.edicao is not None else "")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["edicao"] = self.edicao
        return d

    @staticmethod
    def from_dict(d: dict) -> "Revista":
        obj = Revista(
            d["titulo"],
            d["autor"],
            d["ano"],
            d["genero"],
            d["paginas"],
            d.get("edicao")
        )
        # Restaurar atributos herdados
        obj.status = d.get("status", "NÃO LIDO")
        obj.avaliacao = d.get("avaliacao")
        obj.anotacoes = [Anotacao.from_dict(a) for a in d.get("anotacoes", [])]

        obj.data_inclusao = datetime.fromisoformat(d["data_inclusao"]) if d.get("data_inclusao") else datetime.now()
        obj.data_inicio = datetime.fromisoformat(d["data_inicio"]) if d.get("data_inicio") else None
        obj.data_fim = datetime.fromisoformat(d["data_fim"]) if d.get("data_fim") else None
        return obj
