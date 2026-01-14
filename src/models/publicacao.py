from abc import ABC, abstractmethod
from src.models.anotacao import Anotacao
from datetime import datetime
from exceptions import*

STATUS_VALIDOS = {"NÃO LIDO", "LENDO", "CONCLUIDO"}

class Publicacao(ABC):
    def __init__(self, titulo: str, autor: str, ano: int, genero: str, paginas: int,
                 status: str = "NÃO LIDO", avaliacao: int = None):
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

        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.paginas = paginas
        self.status = status
        self.avaliacao = avaliacao  
        self.data_inclusao = datetime.now()

    def __str__(self):
        return f"{self.tipo()} - {self.titulo} ({self.ano}) [{self.status}]"

    def __repr__(self):
        return (f"<{self.__class__.__name__} titulo='{self.titulo}', autor='{self.autor}', "
                f"ano={self.ano}, genero='{self.genero}', paginas={self.paginas}, "
                f"status='{self.status}', avaliacao={self.avaliacao}>")

    def __eq__(self, other):
        if not isinstance(other, Publicacao):
            return False
        return (self.titulo.lower(), self.autor.lower()) == (other.titulo.lower(), other.autor.lower())

    def __lt__(self, other):
        if not isinstance(other, Publicacao):
            return NotImplemented
        return self.ano < other.ano

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, value):
        if not value or not value.strip():
            raise ValueError("Título não pode ser vazio.")
        self.__titulo = value.strip()

    @property
    def autor(self):
        return self.__autor

    @autor.setter
    def autor(self, value):
        if not value or not value.strip():
            raise ValueError("Autor não pode ser vazio.")
        self.__autor = value.strip()

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, value):
        if not isinstance(value, int) or value < 1500:
            raise ValueError("Ano deve ser maior ou igual a 1500.")
        self.__ano = value

    @property
    def genero(self):
        return self.__genero
    
    @genero.setter
    def genero(self, value):
        if not value or not value.strip():
            raise ValueError ("Gênero não pode ser vazio")
        self.__genero = value.strip()
    
    @property
    def paginas(self):
        return self.__paginas
    
    @paginas.setter
    def paginas(self, value):
        if not isinstance (value, int) or value <= 0:
            raise ValueError("Número de páginas deve ser positivo")
        self.__paginas = value


    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in STATUS_VALIDOS:
            raise ValueError(f"Status inválido. Use {STATUS_VALIDOS}.")
        self.__status = value

    @property
    def avaliacao(self):
        return self.__avaliacao

    @avaliacao.setter
    def avaliacao(self, value):
        if value is None:
            self.__avaliacao = None
            return
        if not isinstance(value, int) or not (1 <= value <= 10):
            raise ValueError("Avaliação deve ser um inteiro entre 1 e 10.")
        # Só avalia se concluído
        if self.status != "CONCLUIDO":
            raise ValueError("Só é possível avaliar quando o status for CONCLUIDO.")
        self.__avaliacao = value

    @property
    def anotacoes(self):
        return list(self.__anotacoes)
    
    @property
    def data_inicio(self): return self.__data_inicio

    @property
    def data_fim(self): return self.__data_fim

    #MÉTODOS DE NEGÓCIO
    def adicionar_anotacao(self, texto, trecho=None):
        if not texto or not texto.strip():
            raise ValueError("Anotação não pode ser vazia.")
        self.__anotacoes.append({"texto": texto.strip(), "trecho": (trecho or None)})

    # MÉTODOS DE STATUS
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


    # SERIALIZAÇÃO
    def to_dict(self):
        return {
            "tipo": self.tipo(),
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
            "anotacoes": self.anotacoes,
        }

    @staticmethod
    def normalizar_chave(titulo, autor, ano, tipo):
        return f"{tipo}|{titulo.strip().lower()}|{autor.strip().lower()}|{ano}"

    @abstractmethod
    def tipo(self):
        ...

class Livro(Publicacao):
    def tipo(self):
        return "Livro"

class Revista(Publicacao):
    def tipo(self):
        return "Revista"
