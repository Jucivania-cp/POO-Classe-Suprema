from datetime import datetime
from src.models.exceptions import InvalidAnnotationError

class Anotacao:
    """
    Representa uma anotação associada a uma publicação.
    
    A anotação contém um texto obrigatório, um trecho opcional e a data de criação.
    """

    def __init__(self, texto: str, trecho: str = None) -> None:
        """
        Inicializa uma anotação.

        :para texto: Texto principal da anotação (não pode ser vazio).
        :para trecho: Trecho opcional da publicação relacionado à anotação.
        :raises InvalidAnnotationError: Se o texto for vazio ou apenas espaços.
        """
        if not texto or not texto.strip():
            raise InvalidAnnotationError("Texto da anotação não pode ser vazio.")
        self.texto: str = texto.strip()
        self.trecho: str | None = trecho
        self.data: datetime = datetime.now()

    def __str__(self) -> str:
        """
        Retorna uma representação amigável da anotação.

        :return: String formatada com data e texto.
        """
        return f"[{self.data.strftime('%d/%m/%Y %H:%M')}] {self.texto}"

    def __repr__(self) -> str:
        """
        Retorna uma representação detalhada para depuração.

        :return: String com atributos principais da anotação.
        """
        return f"<Anotacao texto='{self.texto}', trecho='{self.trecho}', data='{self.data}'>"

    def to_dict(self) -> dict:
        """
        Serializa a anotação para um dicionário.

        :return: Dicionário com texto, trecho e data em formato ISO.
        """
        return {
            "texto": self.texto,
            "trecho": self.trecho,
            "data": self.data.isoformat()
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Anotacao":
        """
        Cria uma instância de Anotacao a partir de um dicionário.

        :para dados: Dicionário com chaves 'texto', 'trecho' e 'data'.
        :return: Objeto Anotacao reconstruído.
        """
        obj = cls(dados["texto"], dados.get("trecho"))
        obj.data = datetime.fromisoformat(dados["data"])
        return obj

