from abc import ABC, abstractmethod
from datetime import datetime

class EstadoLeitura(ABC):
    """Classe base abstrata para os estados de leitura [1]."""

    @abstractmethod
    def iniciar(self, publicacao):
        pass

    @abstractmethod
    def concluir(self, publicacao):
        pass

    @abstractmethod
    def avaliar(self, publicacao, nota):
        pass

    def to_dict(self):
        """Retorna a representação em string do estado para persistência [3]."""
        return self.__class__.__name__

    @staticmethod
    def from_str(nome_estado):
        """Método de fábrica para recriar o estado a partir de uma string."""
        mapa = {
            "NaoLido": NaoLido(),
            "Lendo": Lendo(),
            "Lido": Lido()
        }
        return mapa.get(nome_estado, NaoLido())

class NaoLido(EstadoLeitura):
    def iniciar(self, publicacao):
        # Regra: Iniciar leitura registra a data de início [4]
        publicacao.data_inicio = datetime.now()
        publicacao._status = "LENDO"
        publicacao.estado_atual = Lendo()

    def concluir(self, publicacao):
        # Regra: Não pode marcar como LIDO sem data de início [5]
        raise ValueError("Não é possível concluir uma leitura que não foi iniciada.")

    def avaliar(self, publicacao, nota):
        # Regra: Avaliação só após o status ser LIDO [5]
        raise ValueError("A publicação deve estar 'LIDA' para ser avaliada.")

class Lendo(EstadoLeitura):
    def iniciar(self, publicacao):
        print("A leitura já está em andamento.")

    def concluir(self, publicacao):
        # Regra: Concluir leitura registra a data de término [4]
        publicacao.data_fim = datetime.now()
        publicacao._status = "LIDO"
        publicacao.estado_atual = Lido()

    def avaliar(self, publicacao, nota):
        raise ValueError("Conclua a leitura antes de avaliar.")

class Lido(EstadoLeitura):
    def iniciar(self, publicacao):
        raise ValueError("Esta publicação já foi concluída.")

    def concluir(self, publicacao):
        print("A publicação já está com status LIDO.")

    def avaliar(self, publicacao, nota):
        # Validação de nota 0-10 feita pela @property em Publicacao [6]
        publicacao.avaliacao = nota 