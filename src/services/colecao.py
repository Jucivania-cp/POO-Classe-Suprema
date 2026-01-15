from typing import List
from statistics import mean
from src.models.publicacao import Publicacao, STATUS_NAO_LIDO, STATUS_LENDO, STATUS_CONCLUIDO
from src.models.exceptions import DuplicatedPublicationError

class Colecao:
    def __init__(self, repositorio) -> None:
        self.repositorio = repositorio
        self.publicacoes: List[Publicacao] = repositorio.carregar()

    def adicionar(self, pub: Publicacao) -> None:
        if any(p == pub for p in self.publicacoes):
            raise DuplicatedPublicationError(
                f"Já existe uma publicação com título '{pub.titulo}' e autor '{pub.autor}'."
            )
        self.publicacoes.append(pub)
        self.repositorio.salvar(self.publicacoes)

    def remover(self, pub: Publicacao) -> None:
        if pub in self.publicacoes:
            self.publicacoes.remove(pub)
            self.repositorio.salvar(self.publicacoes)

    def listar(self) -> List[Publicacao]:
        return list(self.publicacoes)

    # Relatórios
    def total_publicacoes(self) -> int:
        return len(self.publicacoes)

    def contagem_por_status(self) -> dict:
        cont = {STATUS_NAO_LIDO: 0, STATUS_LENDO: 0, STATUS_CONCLUIDO: 0}
        for p in self.publicacoes:
            cont[p.status] += 1
        return cont

    def percentual_por_status(self) -> dict:
        total = len(self.publicacoes)
        if total == 0:
            return {}
        cont = self.contagem_por_status()
        return {s: (qtd / total) * 100 for s, qtd in cont.items()}

    def medias_avaliacoes(self) -> dict:
        avaliadas = [p.avaliacao for p in self.publicacoes if p.avaliacao is not None]
        media_geral = mean(avaliadas) if avaliadas else None
        por_status = {}
        for st in (STATUS_NAO_LIDO, STATUS_LENDO, STATUS_CONCLUIDO):
            vals = [p.avaliacao for p in self.publicacoes if p.status == st and p.avaliacao is not None]
            por_status[st] = mean(vals) if vals else None
        return {"geral": media_geral, "por_status": por_status}

    def top5_avaliados(self) -> List[Publicacao]:
        avaliadas = [p for p in self.publicacoes if p.avaliacao is not None]
        return sorted(avaliadas, key=lambda p: p.avaliacao, reverse=True)[:5]
