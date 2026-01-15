import json
from typing import Any

class Settings:
    """
    Carrega e gerencia configurações globais do sistema a partir de settings.json.
    """

    def __init__(self, caminho: str = "data/settings.json") -> None:
        self.caminho = caminho
        self.config: dict[str, Any] = {}
        self.carregar()

    def carregar(self) -> None:
        """
        Carrega configurações do arquivo JSON.
        """
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # valores padrão se não existir settings.json
            self.config = {
                "genero_favorito": None,
                "limite_leituras_simultaneas": 3,
                "meta_anual": 10
            }

    @property
    def genero_favorito(self) -> str | None:
        return self.config.get("genero_favorito")

    @property
    def limite_leituras_simultaneas(self) -> int:
        return self.config.get("limite_leituras_simultaneas", 3)

    @property
    def meta_anual(self) -> int:
        return self.config.get("meta_anual", 10)
