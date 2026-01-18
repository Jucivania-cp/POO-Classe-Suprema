from typing import List
from statistics import mean
from src.models.publicacao import Publicacao, STATUS_NAO_LIDO, STATUS_LENDO, STATUS_CONCLUIDO
from src.models.exceptions import DuplicatedPublicationError

class Colecao:
    def __init__(self, repositorio) -> None:
        self.repositorio = repositorio
        self.publicacoes = repositorio.carregar()

    def adicionar(self, pub: Publicacao) -> None:
        if pub is None:
            raise ValueError("Publicação inválida (None).")
        if any(p == pub for p in self.publicacoes):
            raise DuplicatedPublicationError(
                f"Já existe uma publicação com título '{pub.titulo}' e autor '{pub.autor}'."
            )
        self.publicacoes.append(pub)
        self.repositorio.salvar(self.publicacoes)

    def listar(self): return self.publicacoes

    def remover(self, pub: Publicacao):
        self.publicacoes.remove(pub)
        self.repositorio.salvar(self.publicacoes)


    # Relatórios
    def total_publicacoes(self) -> int:
        return len(self.publicacoes)

    def estatisticas_leitura(self) -> dict:
        total = len(self.publicacoes)
        if total == 0:
            return {"NÃO LIDO": (0, 0.0), "LENDO": (0, 0.0), "CONCLUIDO": (0, 0.0)}

        counts = {
            STATUS_NAO_LIDO: sum(1 for p in self.publicacoes if p.status == STATUS_NAO_LIDO),
            STATUS_LENDO: sum(1 for p in self.publicacoes if p.status == STATUS_LENDO),
            STATUS_CONCLUIDO: sum(1 for p in self.publicacoes if p.status == STATUS_CONCLUIDO),
        }
        return {k: (v, v/total*100) for k, v in counts.items()}

    def media_avaliacoes(self) -> float | None:
        notas = [p.avaliacao for p in self.publicacoes if p.status == STATUS_CONCLUIDO and p.avaliacao is not None]
        return mean(notas) if notas else None

    def top5_avaliadas(self) -> list:
        concluidas = [p for p in self.publicacoes if p.avaliacao is not None]
        return sorted(concluidas, key=lambda p: p.avaliacao, reverse=True)[:5]
