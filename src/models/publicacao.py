from datetime import datetime
from src.models.exceptions import InvalidStatusTransitionError, InvalidEvaluationError
from src.models.anotacao import Anotacao

STATUS_NAO_LIDO = "NÃO LIDO"
STATUS_LENDO = "LENDO"
STATUS_CONCLUIDO = "CONCLUIDO"

class Publicacao:
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int) -> None:
        # atributos encapsulados
        self._titulo = titulo
        self._autor = autor
        self.ano = ano
        self.genero = genero
        self.paginas = paginas

        self._status = STATUS_NAO_LIDO
        self._avaliacao: float | None = None
        self.anotacoes: list[Anotacao] = []

        # ciclo de leitura
        self.data_inclusao = datetime.now()
        self.data_inicio: datetime | None = None
        self.data_fim: datetime | None = None

    # ---------------- PROPERTIES ----------------
    @property
    def titulo(self) -> str:
        return self._titulo
    
    @titulo.setter
    def titulo(self, value):
        if not value or not value.strip():
            raise ValueError("Título não pode ser vazio.")
        self.__titulo = value.strip()

    @property
    def autor(self) -> str:
        return self._autor
    
    @autor.setter
    def autor(self, value):
        if not value or not value.strip():
            raise ValueError("Autor não pode ser vazio.")
        self.__autor = value.strip()

    @property
    def ano(self) -> int:
        return self._ano

    @ano.setter
    def ano(self, valor: int) -> None:
        if valor < 1500:
            raise ValueError("Ano deve ser ≥ 1500.")
        self._ano = valor

    @property
    def genero(self) -> str:
        return self._genero

    @genero.setter
    def genero(self, valor: str) -> None:
        self._genero = valor

    @property
    def paginas(self) -> int:
        return self._paginas

    @paginas.setter
    def paginas(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("Número de páginas deve ser positivo.")
        self._paginas = valor

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, novo: str) -> None:
        if novo not in {STATUS_NAO_LIDO, STATUS_LENDO, STATUS_CONCLUIDO}:
            raise ValueError("Status inválido.")

        # regras de negócio
        if novo == STATUS_LENDO:
            if self.data_inicio is None:
                self.data_inicio = datetime.now()

        if novo == STATUS_CONCLUIDO:
            if self.data_inicio is None:
                raise InvalidStatusTransitionError("Não é possível concluir sem data de início.")
            self.data_fim = datetime.now()

        self._status = novo

    @property
    def avaliacao(self) -> float | None:
        return self._avaliacao

    @avaliacao.setter
    def avaliacao(self, nota: float | None) -> None:
        if nota is None:
            self._avaliacao = None
            return
        if not (0 <= nota <= 10):
            raise InvalidEvaluationError("A avaliação deve estar entre 0 e 10.")
        if self.data_fim is None:
            raise InvalidEvaluationError("Só é possível avaliar após concluir a leitura.")
        self._avaliacao = float(nota)

    # ---------------- MÉTODOS DE NEGÓCIO ----------------
    def iniciar_leitura(self) -> None:
        self.status = STATUS_LENDO

    def concluir_leitura(self) -> None:
        self.status = STATUS_CONCLUIDO

    def adicionar_anotacao(self, anot: Anotacao) -> None:
        self.anotacoes.append(anot)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Publicacao):
            return False
        return (self.titulo.lower(), self.autor.lower()) == (other.titulo.lower(), other.autor.lower())

    def __str__(self) -> str:
        base = f"{self.titulo} — {self.autor} ({self.ano}) [{self.genero}] {self.paginas}p"
        status = f" | Status: {self.status}"
        nota = f" | Nota: {self.avaliacao}" if self.avaliacao is not None else ""
        datas = ""
        if self.data_inicio or self.data_fim:
            di = self.data_inicio.strftime("%Y-%m-%d %H:%M") if self.data_inicio else "-"
            df = self.data_fim.strftime("%Y-%m-%d %H:%M") if self.data_fim else "-"
            datas = f" | Início: {di} | Fim: {df}"
        return base + status + nota + datas

    # ---------------- PERSISTÊNCIA ----------------
    def to_dict(self) -> dict:
        return {
            "tipo": self.__class__.__name__,
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "genero": self.genero,
            "paginas": self.paginas,
            "status": self.status,
            "avaliacao": self.avaliacao,
            "anotacoes": [a.to_dict() for a in self.anotacoes],
            "data_inclusao": self.data_inclusao.isoformat(),
            "data_inicio": self.data_inicio.isoformat() if self.data_inicio else None,
            "data_fim": self.data_fim.isoformat() if self.data_fim else None,
        }

    @staticmethod
    def from_dict(d: dict) -> "Publicacao":
        tipo = d.get("tipo", "Publicacao")
        if tipo == "Livro":
            from src.models.livro import Livro
            obj = Livro(d["titulo"], d["autor"], d["ano"], d["genero"], d["paginas"], d.get("isbn"))
        elif tipo == "Revista":
            from src.models.revista import Revista
            obj = Revista(d["titulo"], d["autor"], d["ano"], d["genero"], d["paginas"], d.get("edicao"))
        else:
            obj = Publicacao(d["titulo"], d["autor"], d["ano"], d["genero"], d["paginas"])

        obj.status = d.get("status", STATUS_NAO_LIDO)
        obj.avaliacao = d.get("avaliacao")
        obj.anotacoes = [Anotacao.from_dict(a) for a in d.get("anotacoes", [])]

        obj.data_inclusao = datetime.fromisoformat(d["data_inclusao"]) if d.get("data_inclusao") else datetime.now()
        obj.data_inicio = datetime.fromisoformat(d["data_inicio"]) if d.get("data_inicio") else None
        obj.data_fim = datetime.fromisoformat(d["data_fim"]) if d.get("data_fim") else None
        return obj

