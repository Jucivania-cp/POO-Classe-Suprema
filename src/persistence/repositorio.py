from src.persistence.dados import carregar_publicacoes, salvar_publicacoes, adicionar_publicacao
from src.models.publicacao import Publicacao

class Repositorio:
    def __init__(self, arquivo="publicacoes.json"):
        self.arquivo = arquivo
        self.publicacoes = carregar_publicacoes(arquivo)

    # ---------------- CRUD ----------------
    def adicionar(self, publicacao: Publicacao):
        adicionar_publicacao(self.publicacoes, publicacao, self.arquivo)

    def listar(self):
        return list(self.publicacoes)

    def buscar_por_titulo(self, titulo: str):
        return [p for p in self.publicacoes if p.titulo.lower() == titulo.lower()]

    def buscar_por_autor(self, autor: str):
        return [p for p in self.publicacoes if p.autor.lower() == autor.lower()]

    def buscar_por_ano(self, ano: int):
        return [p for p in self.publicacoes if p.ano == ano]

    def remover(self, publicacao: Publicacao):
        if publicacao in self.publicacoes:
            self.publicacoes.remove(publicacao)
            salvar_publicacoes(self.publicacoes, self.arquivo)

    # ---------------- RELATÓRIOS ----------------
    def listar_por_status(self, status: str):
        return [p for p in self.publicacoes if p.status == status]

    def listar_por_tipo(self, tipo: str):
        return [p for p in self.publicacoes if p.tipo().lower() == tipo.lower()]

    def listar_ordenado_por_ano(self):
        return sorted(self.publicacoes, key=lambda p: p.ano)

    def listar_ordenado_por_data_inclusao(self):
        return sorted(self.publicacoes, key=lambda p: p.data_inclusao)

    def relatorio_avaliacoes(self):
        return {p.titulo: p.avaliacao for p in self.publicacoes if p.avaliacao is not None}
