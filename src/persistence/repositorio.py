import os
import json
from src.models.publicacao import Livro, Revista

class RepositorioJSON:
    def __init__(self, arquivo="data/biblioteca.json"):
        self.arquivo = arquivo
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)

    def salvar(self, publicacoes):
        dados = [p.to_dict() for p in publicacoes]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar(self):
        if not os.path.exists(self.arquivo):
            return []
        with open(self.arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        pubs = []
        for d in dados:
            if d["tipo"] == "Livro":
                pub = Livro(d["titulo"], d["autor"], d["ano"], d["status"], d["avaliacao"])
            else:
                pub = Revista(d["titulo"], d["autor"], d["ano"], d["status"], d["avaliacao"])
            for a in d.get("anotacoes", []):
                pub.adicionar_anotacao(a["texto"], a.get("trecho"))
            pubs.append(pub)
        return pubs
