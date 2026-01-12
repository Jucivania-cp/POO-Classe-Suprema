from src.models.publicacao import Publicacao

class Colecao:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.publicacoes = repositorio.carregar()
        self._reindexar()

    def _reindexar(self):
        self._index = {
            Publicacao.normalizar_chave(p.titulo, p.autor, p.ano, p.tipo()): i
            for i, p in enumerate(self.publicacoes)
        }

    def _chave(self, pub):
        return Publicacao.normalizar_chave(pub.titulo, pub.autor, pub.ano, pub.tipo())

    def adicionar(self, publicacao):
        chave = self._chave(publicacao)
        if chave in self._index:
            raise ValueError("Já existe uma publicação com mesmo título, autor, ano e tipo.")
        self.publicacoes.append(publicacao)
        self._reindexar()
        self.repositorio.salvar(self.publicacoes)

    def listar(self):
        return list(self.publicacoes)

    def buscar(self, titulo, autor, ano, tipo):
        chave = Publicacao.normalizar_chave(titulo, autor, ano, tipo)
        idx = self._index.get(chave)
        return self.publicacoes[idx] if idx is not None else None

    def iniciar(self, titulo, autor, ano, tipo):
        pub = self.buscar(titulo, autor, ano, tipo)
        if not pub:
            raise ValueError("Publicação não encontrada.")
        pub.iniciar_leitura()
        self.repositorio.salvar(self.publicacoes)

    def concluir(self, titulo, autor, ano, tipo, avaliacao=None):
        pub = self.buscar(titulo, autor, ano, tipo)
        if not pub:
            raise ValueError("Publicação não encontrada.")
        pub.concluir_leitura(avaliacao)
        self.repositorio.salvar(self.publicacoes)

    def abandonar(self, titulo, autor, ano, tipo):
        pub = self.buscar(titulo, autor, ano, tipo)
        if not pub:
            raise ValueError("Publicação não encontrada.")
        pub.abandonar()
        self.repositorio.salvar(self.publicacoes)

    def anotar(self, titulo, autor, ano, tipo, texto, trecho=None):
        pub = self.buscar(titulo, autor, ano, tipo)
        if not pub:
            raise ValueError("Publicação não encontrada.")
        pub.adicionar_anotacao(texto, trecho)
        self.repositorio.salvar(self.publicacoes)
