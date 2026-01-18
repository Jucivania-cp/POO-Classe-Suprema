import json, os
from src.models.livro import Livro
from src.models.revista import Revista

class RepositorioJSON:
    def __init__(self, arquivo="data/biblioteca.json"):
        self.arquivo = arquivo

    def salvar(self, publicacoes):
        dados = [p.to_dict() for p in publicacoes]
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar(self):
        if not os.path.exists(self.arquivo): return []
        with open(self.arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        pubs = []
        for d in dados:
            if d["tipo"] == "Livro": pubs.append(Livro.from_dict(d))
            elif d["tipo"] == "Revista": pubs.append(Revista.from_dict(d))
        return pubs

