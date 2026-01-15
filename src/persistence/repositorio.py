import json, os
from src.models.publicacao import Publicacao
from src.models.exceptions import DuplicatedPublicationError

class RepositorioJSON:
    def __init__(self, arquivo="biblioteca.json") -> None:
        self.arquivo = arquivo

    def salvar(self, publicacoes):
        dados = [pub.to_dict() for pub in publicacoes]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar(self):
        if not os.path.exists(self.arquivo):
            return []
        with open(self.arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return [Publicacao.from_dict(d) for d in dados]

    def adicionar(self, publicacoes, nova_publicacao):
        if nova_publicacao in publicacoes:
            raise DuplicatedPublicationError(
                f"Já existe uma publicação com título '{nova_publicacao.titulo}' e autor '{nova_publicacao.autor}'."
            )
        publicacoes.append(nova_publicacao)
        self.salvar(publicacoes)
