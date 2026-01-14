import json
import os
from src.models.publicacao import Publicacao
from src.models.exceptions import DuplicatedPublicationError

ARQUIVO_JSON = "publicacoes.json"

def salvar_publicacoes(publicacoes, arquivo=ARQUIVO_JSON):
    """
    Salva a lista de publicações em um arquivo JSON.
    """
    dados = [pub.to_dict() for pub in publicacoes]
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def carregar_publicacoes(arquivo=ARQUIVO_JSON):
    """
    Carrega publicações de um arquivo JSON e recria os objetos.
    """
    if not os.path.exists(arquivo):
        return []

    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return [Publicacao.from_dict(d) for d in dados]


def adicionar_publicacao(publicacoes, nova_publicacao, arquivo=ARQUIVO_JSON):
    """
    Adiciona uma nova publicação à lista, evitando duplicados.
    """
    if nova_publicacao in publicacoes:
        raise DuplicatedPublicationError(
            f"Já existe uma publicação com título '{nova_publicacao.titulo}' e autor '{nova_publicacao.autor}'."
        )

    publicacoes.append(nova_publicacao)
    salvar_publicacoes(publicacoes, arquivo)
