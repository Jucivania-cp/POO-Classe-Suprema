from datetime import datetime
from src.models.exceptions import InvalidAnnotationError

class Anotacao:
    def __init__(self, texto: str, trecho: str | None = None) -> None:
        if not texto or not texto.strip():
            raise InvalidAnnotationError("Texto da anotação não pode ser vazio.")
        self._texto = texto.strip()
        self._trecho = trecho
        self._data = datetime.now()

    @property
    def texto(self) -> str:
        return self._texto

    @property
    def trecho(self) -> str | None:
        return self._trecho

    @property
    def data(self) -> datetime:
        return self._data

    def __str__(self) -> str:
        base = f"[{self.data.strftime('%Y-%m-%d %H:%M')}] {self.texto}"
        return f"{base} — Trecho: {self.trecho}" if self.trecho else base

    def to_dict(self) -> dict:
        return {
            "texto": self.texto,
            "trecho": self.trecho,
            "data": self.data.isoformat()
        }

    @staticmethod
    def from_dict(d: dict) -> "Anotacao":
        obj = Anotacao(d["texto"], d.get("trecho"))
        obj._data = datetime.fromisoformat(d["data"]) if "data" in d else datetime.now()
        return obj
