from abc import ABC, abstractmethod
from datetime import datetime
from src.models.anotacao import Anotacao
from src.models.exceptions import InvalidStatusTransitionError, InvalidEvaluationError

STATUS_NAO_LIDO = "NÃO LIDO"
STATUS_LENDO = "LENDO"
STATUS_CONCLUIDO = "CONCLUIDO"

class Publicacao(ABC):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int) -> None:
        if not titulo.strip():
            raise ValueError("Título não pode ser vazio.")
        if not autor.strip():
            raise ValueError("Autor não pode ser vazio.")
        if ano < 1500:
            raise ValueError("Ano deve ser maior ou igual a 1500.")
        if paginas <= 0:
            raise ValueError("Número de páginas deve ser positivo.")

        self._titulo = titulo
        self._autor = autor
        self._ano = ano
        self._genero = genero
        self._paginas = paginas

        self._status = STATUS_NAO_LIDO
        self._avaliacao: float | None = None
        self.anotacoes: list[Anotacao] = []

        self.data_inclusao = datetime.now()
        self.data_inicio: datetime | None = None
        self.data_fim: datetime | None = None

    @property
    def titulo(self): return self._titulo
    @property
    def autor(self): return self._autor
    @property
    def ano(self): return self._ano
    @property
    def genero(self): return self._genero
    @property
    def paginas(self): return self._paginas

    @property
    def status(self): return self._status
    @status.setter
    def status(self, novo: str):
        if novo == STATUS_LENDO and self.data_inicio is None:
            self.data_inicio = datetime.now()
        if novo == STATUS_CONCLUIDO:
            if self.data_inicio is None:
                raise InvalidStatusTransitionError("Não é possível concluir sem iniciar leitura.")
            self.data_fim = datetime.now()
        self._status = novo

    @property
    def avaliacao(self): return self._avaliacao
    @avaliacao.setter
    def avaliacao(self, nota: float | None):
        if nota is None: self._avaliacao = None; return
        if not (0 <= nota <= 10): raise InvalidEvaluationError("Nota deve estar entre 0 e 10.")
        if self.data_fim is None: raise InvalidEvaluationError("Só pode avaliar após concluir leitura.")
        self._avaliacao = float(nota)

    def iniciar_leitura(self) -> None:
        self.status = STATUS_LENDO  # registra data_inicio automaticamente

    def concluir_leitura(self) -> None:
        self.status = STATUS_CONCLUIDO  # valida início e registra data_fim

    def adicionar_anotacao(self, anot: Anotacao): self.anotacoes.append(anot)

    def __eq__(self, other):
        return isinstance(other, Publicacao) and \
               (self.titulo.lower(), self.autor.lower()) == (other.titulo.lower(), other.autor.lower())

    def __str__(self):
        return f"{self.titulo} — {self.autor} ({self.ano}) [{self.genero}] {self.paginas}p | Status: {self.status}"

    @abstractmethod
    def to_dict(self) -> dict: ...
    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> "Publicacao": ...
