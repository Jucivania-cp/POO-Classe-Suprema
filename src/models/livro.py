from src.models.publicacao import Publicacao
from src.models.anotacao import Anotacao
from datetime import datetime

class Livro(Publicacao):
    def __init__(self, titulo, autor, ano, genero, paginas, isbn=None):
        super().__init__(titulo, autor, ano, genero, paginas)
        self._isbn = isbn

    @property
    def isbn(self): return self._isbn

    def to_dict(self) -> dict:
        d = {
            "tipo": "Livro",
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "genero": self.genero,
            "paginas": self.paginas,
            "isbn": self.isbn,
            "status": self.status,
            "avaliacao": self.avaliacao,
            "anotacoes": [a.to_dict() for a in self.anotacoes],
            "data_inclusao": self.data_inclusao.isoformat(),
            "data_inicio": self.data_inicio.isoformat() if self.data_inicio else None,
            "data_fim": self.data_fim.isoformat() if self.data_fim else None,
        }
        return d

    @staticmethod
    def from_dict(d: dict) -> "Livro":
        obj = Livro(d["titulo"], d["autor"], d["ano"], d["genero"], d["paginas"], d.get("isbn"))
        obj._status = d.get("status", "NÃO LIDO")
        obj._avaliacao = d.get("avaliacao")
        obj.anotacoes = [Anotacao.from_dict(a) for a in d.get("anotacoes", [])]
        obj.data_inclusao = datetime.fromisoformat(d["data_inclusao"]) if d.get("data_inclusao") else datetime.now()
        obj.data_inicio = datetime.fromisoformat(d["data_inicio"]) if d.get("data_inicio") else None
        obj.data_fim = datetime.fromisoformat(d["data_fim"]) if d.get("data_fim") else None
        return obj
