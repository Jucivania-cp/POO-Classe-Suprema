from abc import ABC, abstractmethod
from datetime import datetime

class Publicacao(ABC):
    def __init__ (self, titulo, autor, ano, genero, paginas):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.paginas = paginas
        self._status = "NÃO LIDO"
        self._avaliacao = 0.0
        self.data_inclusao
        self.data_fim
        self.anotacoes = []

    @property
    def titulo(self):
        return self._titulo
    
    @titulo.setter
    def titulo(self, valor):
        if not valor or not valor.strip():
            raise ValueError ("O título não pode ser vazio")
        self._titulo = valor

    @property
    def ano(self):
        return self._ano
    
    @ano.setter
    def ano (self, valor):
        if valor < 1500:
            raise ValueError ("O ano de publicação deve ser maior ou igual a 1500")
        self._ano = valor

    @property
    def avaliacao(self):
        return self._avaliacao
    
    @avaliacao.setter
    def avaliacao (self, valor):
        if self._status != "LIDO":
            raise ValueError ("Avaliação só pode ser feita após o status ser 'LIDO'")
        if not (0 <= valor <= 10):
            raise ValueError ("A nota deve estar entre 0 e 10")
        self._avaliacao = valor

    @property
    def status(self):
        return self._status

# --- MÉTODOS DE NEGÓCIO ---
    def iniciar_leitura(self):
        self._status = "LENDO"
        self.data_inicio = datetime.now()

    def concluir_leitura(self):
        if not self.data_inicio:
            raise ValueError("Não pode ser marcada como LIDA sem data de início [8, 11].")
        self._status = "LIDO"
        self.data_fim = datetime.now()

    # --- PERSISTÊNCIA ---
    def to_dict(self):
        """Converte o objeto em dicionário para o JSON [7]."""
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "genero": self.genero,
            "paginas": self.paginas,
            "status": self._status,
            "avaliacao": self._avaliacao,
            "data_inclusao": self.data_inclusao.isoformat() if isinstance(self.data_inclusao, datetime) else self.data_inclusao,
            "data_inicio": self.data_inicio.isoformat() if isinstance(self.data_inicio, datetime) else self.data_inicio,
            "data_fim": self.data_fim.isoformat() if isinstance(self.data_fim, datetime) else self.data_fim
        }

    @classmethod
    def from_dict(cls, dados):
        """Método fábrica que decide qual classe filha instanciar [1]."""
        tipo = dados.get('tipo')
        
        if tipo == 'livro':
            return Livro.from_dict(dados)
        elif tipo == 'revista':
            return Revista.from_dict(dados)
        raise ValueError(f"Tipo '{tipo}' desconhecido [1].")

    # --- MÉTODOS ESPECIAIS ---
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.ano}) | Status: {self.status}"

    def __repr__(self):
        return f"Publicacao(titulo='{self.titulo}', status='{self.status}')"

    def __lt__(self, outro):
        return self.ano < outro.ano

    def __eq__(self, outro):
        if not isinstance(outro, Publicacao): return False
        return (self.titulo.lower() == outro.titulo.lower() and 
                self.autor.lower() == outro.autor.lower())

class Livro(Publicacao):
    def __init__(self, titulo, autor, ano, genero, paginas,isbn):
        super.__init__(self, titulo, autor, ano, genero, paginas)
        self.isbn = isbn

    def to_dict(self):
        dados = super().to_dict()
        dados["tipo"] = "livro"
        dados["extra"] = self.isbn [12]
        return dados

    @classmethod
    def from_dict(cls, dados):
        obj = cls(dados['titulo'], dados['autor'], dados['ano'], 
                  dados['genero'], dados['paginas'], dados.get('extra'))
        # Restaura estados sem disparar validações de fluxo [2]
        obj._status = dados.get('status')
        obj._avaliacao = dados.get('avaliacao', 0.0)
        obj.data_inclusao = dados.get('data_inclusao')
        obj.data_inicio = dados.get('data_inicio')
        obj.data_fim = dados.get('data_fim')
        return obj

    
class Revista(Publicacao):
    def __init__(self, titulo, autor, ano, genero, paginas,edicao):
        super.__init__(self, titulo, autor, ano, genero, paginas)
        self.edicao = edicao

    def __str__(self):
        return f"[REVISTA] {super().__str__()} | EDIÇÃO: {self.edicao}"

  def to_dict(self):
        dados = super().to_dict()
        dados["tipo"] = "revista"
        dados["extra"] = self.edicao [13]
        return dados

    @classmethod
    def from_dict(cls, dados):
        obj = cls(dados['titulo'], dados['autor'], dados['ano'], 
                  dados['genero'], dados['paginas'], dados.get('extra'))
        # Restaura estados e datas (Corrigido: return no final) [3, 15]
        obj._status = dados.get('status')
        obj._avaliacao = dados.get('avaliacao', 0.0)
        obj.data_inclusao = dados.get('data_inclusao')
        obj.data_inicio = dados.get('data_inicio')
        obj.data_fim = dados.get('data_fim')
        return obj