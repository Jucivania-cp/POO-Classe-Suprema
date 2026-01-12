from abc import ABC, abstractmethod

STATUS_VALIDOS = {"NAO_LIDO", "LENDO", "CONCLUIDO"}

class Publicacao(ABC):
    def __init__(self, titulo, autor, ano, status="NAO_LIDO", avaliacao=None):
        self.__titulo = None
        self.__autor = None
        self.__ano = None
        self.__status = None
        self.__avaliacao = None
        self.__anotacoes = []

        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.status = status
        self.avaliacao = avaliacao  

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
        if not isinstance(value, int) or value < 0:
            raise ValueError("Ano deve ser um inteiro positivo.")
        self.__ano = value

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

    def adicionar_anotacao(self, texto, trecho=None):
        if not texto or not texto.strip():
            raise ValueError("Anotação não pode ser vazia.")
        self.__anotacoes.append({"texto": texto.strip(), "trecho": (trecho or None)})

    # MÉTODOS DE STATUS
    def iniciar_leitura(self):
        self.status = "LENDO"

    def concluir_leitura(self, avaliacao=None):
        self.status = "CONCLUIDO"
        if avaliacao is not None:
            self.avaliacao = avaliacao

  

    # SERIALIZAÇÃO
    def to_dict(self):
        return {
            "tipo": self.tipo(),
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "status": self.status,
            "avaliacao": self.avaliacao,
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
