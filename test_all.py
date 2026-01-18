import pytest
from src.models.livro import Livro
from src.models.exceptions import InvalidStatusTransitionError, InvalidEvaluationError, DuplicatedPublicationError
from src.services.colecao import Colecao
from src.persistence.repositorio import RepositorioJSON


#PUBLICAÇÃO
def test_titulo_autor_nao_podem_ser_vazios():
    with pytest.raises(ValueError):
        Livro("", "Autor", 2000, "Romance", 100)
    with pytest.raises(ValueError):
        Livro("Titulo", "", 2000, "Romance", 100)

def test_ano_deve_ser_maior_que_1500():
    with pytest.raises(ValueError):
        Livro("Titulo", "Autor", 1400, "Romance", 100)

def test_nao_pode_concluir_sem_iniciar():
    livro = Livro("Titulo", "Autor", 2000, "Romance", 100)
    with pytest.raises(InvalidStatusTransitionError):
        livro.concluir_leitura()

def test_avaliacao_somente_apos_concluir():
    livro = Livro("Titulo", "Autor", 2000, "Romance", 100)
    livro.iniciar_leitura()
    with pytest.raises(InvalidEvaluationError):
        livro.avaliacao = 8
    livro.concluir_leitura()
    livro.avaliacao = 9
    assert livro.avaliacao == 9

#COLEÇÃO
def test_nao_aceita_duplicados(tmp_path):
    repo = RepositorioJSON(tmp_path / "bib.json")
    colecao = Colecao(repo)
    livro1 = Livro("Titulo", "Autor", 2000, "Romance", 100)
    colecao.adicionar(livro1)
    livro2 = Livro("Titulo", "Autor", 2000, "Romance", 100)
    with pytest.raises(DuplicatedPublicationError):
        colecao.adicionar(livro2)

#REPOSITORIO
def test_salvar_e_carregar(tmp_path):
    repo = RepositorioJSON(tmp_path / "bib.json")
    livro = Livro("Titulo", "Autor", 2000, "Romance", 100)
    repo.salvar([livro])
    pubs = repo.carregar()
    assert len(pubs) == 1
    assert pubs[0].titulo == "Titulo"

