from abc import ABC, abstractmethod
from datetime import datetime
from .anotacao import Anotacao
from src.models.exceptions import InvalidStatusError, InvalidEvaluationError

STATUS_VALIDOS = {"NÃO LIDO", "LENDO", "CONCLUIDO"}

class Publicacao(ABC):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int,
                 status: str = "NÃO_LIDO", avaliacao: int = None):
        self.__titulo = None
        self.__autor = None
        self.__ano = None
        self.__genero = None
        self.__paginas = None
        self.__status = None
        self.__avaliacao = None
        self.__anotacoes = []
        self.__data_inicio = None
        self.__data_fim = None

        self.data_inclusao = datetime.now()
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.paginas = paginas
        self.status = status
        self.avaliacao = avaliacao

    # ---------------- PROPRIEDADES ----------------
    @property
    def titulo(self): return self.__titulo
    @titulo.setter
    def titulo(self, value):
        if not value or not value.strip():
            raise ValueError("Título não pode ser vazio.")
        self.__titulo = value.strip()

    @property
    def autor(self): return self.__autor
    @autor.setter
    def autor(self, value):
        if not value or not value.strip():
            raise ValueError("Autor não pode ser vazio.")
        self.__autor = value.strip()

    @property
    def ano(self): return self.__ano
    @ano.setter
    def ano(self, value):
        if not isinstance(value, int) or value < 1500:
            raise ValueError("Ano deve ser ≥ 1500.")
        self.__ano = value

    @property
    def genero(self): return self.__genero
    @genero.setter
    def genero(self, value):
        if not value or not value.strip():
            raise ValueError("Gênero não pode ser vazio.")
        self.__genero = value.strip()

    @property
    def paginas(self): return self.__paginas
    @paginas.setter
    def paginas(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Número de páginas deve ser positivo.")
        self.__paginas = value

    @property
    def status(self): return self.__status
    @status.setter
    def status(self, value):
        if value not in STATUS_VALIDOS:
            raise InvalidStatusError(f"Status inválido. Use {STATUS_VALIDOS}.")
        self.__status = value

    @property
    def avaliacao(self): return self.__avaliacao
    @avaliacao.setter
    def avaliacao(self, value):
        if value is None:
            self.__avaliacao = None
            return
        if not isinstance(value, int) or not (0 <= value <= 10):
            raise InvalidEvaluationError("Avaliação deve ser entre 0 e 10.")
        if self.status != "CONCLUIDO":
            raise InvalidEvaluationError("Só é possível avaliar quando o status for CONCLUIDO.")
        self.__avaliacao = value

    @property
    def anotacoes(self): return list(self.__anotacoes)

    @property
    def data_inicio(self): return self.__data_inicio
    @property
    def data_fim(self): return self.__data_fim

    # ---------------- MÉTODOS DE NEGÓCIO ----------------
    def iniciar_leitura(self):
        self.status = "LENDO"
        self.__data_inicio = datetime.now()

    def concluir_leitura(self, avaliacao=None):
        if not self.__data_inicio:
            raise InvalidStatusError("Não é possível concluir sem data de início.")
        self.status = "CONCLUIDO"
        self.__data_fim = datetime.now()
        if avaliacao is not None:
            self.avaliacao = avaliacao

    def adicionar_anotacao(self, anotacao: Anotacao):
        if not isinstance(anotacao, Anotacao):
            raise TypeError("Esperado objeto do tipo Anotacao.")
        self.__anotacoes.append(anotacao)

    @abstractmethod
    def tipo(self): ...
    
    # ---------------- SERIALIZAÇÃO ----------------
    def to_dict(self):
        return {
            "tipo": self.tipo().lower(),
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "genero": self.genero,
            "paginas": self.paginas,
            "status": self.status,
            "avaliacao": self.avaliacao,
            "data_inclusao": self.data_inclusao.isoformat(),
            "data_inicio": self.data_inicio.isoformat() if self.data_inicio else None,
            "data_fim": self.data_fim.isoformat() if self.data_fim else None,
            "anotacoes": [a.to_dict() for a in self.anotacoes],
        }

    @classmethod
    def from_dict(cls, dados):
        tipo = dados.get("tipo")
        if tipo == "livro":
            return Livro.from_dict(dados)
        elif tipo == "revista":
            return Revista.from_dict(dados)
        raise ValueError(f"Tipo '{tipo}' desconhecido.")
    # ---------------------------------------------------

    # ---------------- MÉTODOS ESPECIAIS ----------------
    def __str__(self):
        return f"{self.tipo()} - {self.titulo} ({self.ano}) [{self.status}]"

    def __repr__(self):
        return (f"<{self.__class__.__name__} titulo='{self.titulo}', autor='{self.autor}', "
                f"ano={self.ano}, genero='{self.genero}', paginas={self.paginas}, "
                f"status='{self.status}', avaliacao={self.avaliacao}, "
                f"data_inclusao='{self.data_inclusao}'>")

    def __eq__(self, other):
        if not isinstance(other, Publicacao):
            return False
        return (self.titulo.lower(), self.autor.lower()) == (other.titulo.lower(), other.autor.lower())

    def __lt__(self, other):
        if not isinstance(other, Publicacao):
            return NotImplemented
        return self.ano < other.ano


# ---------------- SUBCLASSE LIVRO ----------------
class Livro(Publicacao):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int,
                 isbn: str, status: str = "NAO_LIDO", avaliacao: int = None):
        super().__init__(titulo, autor, ano, genero, paginas, status, avaliacao)
        self.isbn = isbn

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, value: str):
        if not value or not value.strip():
            raise ValueError("ISBN não pode ser vazio.")
        if len(value.strip()) not in (10, 13):
            raise ValueError("ISBN deve ter 10 ou 13 caracteres.")
        self.__isbn = value.strip()

    def __str__(self):
        return f"{super().__str__()} | ISBN: {self.isbn}"

    def __repr__(self):
        return f"<Livro titulo='{self.titulo}', autor='{self.autor}', ano={self.ano}, isbn='{self.isbn}'>"

    def tipo(self):
        return "Livro"

    def to_dict(self):
        data = super().to_dict()
        data["isbn"] = self.isbn
        return data

    @classmethod
    def from_dict(cls, dados):
        return cls(
            titulo=dados["titulo"],
            autor=dados["autor"],
            ano=dados["ano"],
            genero=dados["genero"],
            paginas=dados["paginas"],
            isbn=dados["isbn"],
            status=dados.get("status", "NAO_LIDO"),
            avaliacao=dados.get("avaliacao"),
        )


# ---------------- SUBCLASSE REVISTA ----------------
class Revista(Publicacao):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int,
                 edicao: int, status: str = "NAO_LIDO", avaliacao: int = None):
        super().__init__(titulo, autor, ano, genero, paginas, status, avaliacao)
        self.edicao = edicao

    @property
    def edicao(self) -> int:
        return self.__edicao

    @edicao.setter
    def edicao(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Edição deve ser um número inteiro positivo.")
        self.__edicao = value

    def __str__(self):
        return f"{super().__str__()} | Edição: {self.edicao}"

    def __repr__(self):
        return f"<Revista titulo='{self.titulo}', autor='{self.autor}', ano={self.ano}, edicao={self.edicao}>"

    def tipo(self):
        return "Revista"

    def to_dict(self):
        data = super().to_dict()
        data["edicao"] = self.edicao
        return data

    @classmethod
    def from_dict(cls, dados):
        return cls(
            titulo=dados["titulo"],
            autor=dados["autor"],
            ano=dados["ano"],
            genero=dados["genero"],
            paginas=dados["paginas"],
            edicao=dados["edicao"],
            status=dados.get("status", "NAO_LIDO"),
            avaliacao=dados.get("avaliacao"),
        )

