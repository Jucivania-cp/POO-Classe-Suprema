import json, os
from src.models.publicacao import Publicacao

class RepositorioJSON:
    def __init__(self, arquivo: str = "data/biblioteca.json") -> None:
        self.arquivo = arquivo

    def salvar(self, publicacoes: list[Publicacao]) -> None:
        dados = [p.to_dict() for p in publicacoes]
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar(self) -> list[Publicacao]:
        if not os.path.exists(self.arquivo):
            return []
        with open(self.arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return [Publicacao.from_dict(d) for d in dados]
