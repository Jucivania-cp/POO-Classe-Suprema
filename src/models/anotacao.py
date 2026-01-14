from datetime import datetime

class Anotacao:
    def __init__(self, texto: str, trecho: str = None):
        if not texto or not texto.strip():
            raise ValueError("Texto da anotação não pode ser vazio.")
        self.texto = texto.strip()
        self.trecho = trecho
        self.data = datetime.now()

    def __str__(self):
        return f"[{self.data.strftime('%d/%m/%Y %H:%M')}] {self.texto}"

    def __repr__(self):
        return f"<Anotacao texto='{self.texto}', trecho='{self.trecho}', data='{self.data}'>"
