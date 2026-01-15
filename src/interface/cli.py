import argparse
from src.models.livro import Livro
from src.models.revista import Revista
from src.models.publicacao import Publicacao
from src.services.colecao import Colecao
from src.persistence.repositorio import RepositorioJSON

# Instancia o repositório e a coleção
repo = RepositorioJSON("data/biblioteca.json")
colecao = Colecao(repo)

# ---------------- SUBCOMANDOS ----------------
def cadastrar(args):
    if args.tipo == "livro":
        pub = Livro(
            titulo=args.titulo,
            autor=args.autor,
            ano=args.ano,
            genero=args.genero,
            paginas=args.paginas,
            isbn=args.isbn
        )
    else:
        pub = Revista(
            titulo=args.titulo,
            autor=args.autor,
            ano=args.ano,
            genero=args.genero,
            paginas=args.paginas,
            edicao=args.edicao
        )
    try:
        colecao.adicionar(pub)
        print("✅ Publicação cadastrada:", pub)
    except Exception as e:
        print("❌ Erro ao cadastrar:", e)

def listar(args):
    pubs = colecao.listar()
    if not pubs:
        print("📭 Nenhuma publicação cadastrada.")
    else:
        print("📚 Publicações:")
        for p in pubs:
            print("-", p)

def anotar(args):
    pubs = colecao.listar()
    if not pubs:
        print("📭 Nenhuma publicação disponível.")
        return
    pub = pubs[0]  # exemplo simples: anotar na primeira publicação
    anot = Anotacao(args.texto, args.trecho)
    pub.adicionar_anotacao(anot)
    colecao.repositorio.salvar(colecao.publicacoes)
    print("📝 Anotação adicionada:", anot)

def relatorio(args):
    print("📊 Relatório:")
    print("Total:", colecao.total_publicacoes())
    print("Percentuais:", colecao.percentual_por_status())
    medias = colecao.medias_avaliacoes()
    print("Média geral das avaliações:", medias["geral"])
    print("Média por status:", medias["por_status"])
    print("Contagem por status:", colecao.contagem_por_status())
    print("Percentual por status:", colecao.percentual_por_status())
    top5 = colecao.top5_avaliados()
    if not top5:
        print("Nenhuma publicação avaliada ainda.")
    else:
        print("Top 5 mais bem avaliados:")
        for p in top5:
            print("-", p)

def buscar(args):
    resultados = []
    if args.titulo:
        resultados = colecao.buscar_por_titulo(args.titulo)
    elif args.autor:
        resultados = colecao.buscar_por_autor(args.autor)
    elif args.genero:
        resultados = colecao.buscar_por_genero(args.genero)
    elif args.status:
        resultados = colecao.buscar_por_status(args.status)

    if not resultados:
        print("📭 Nenhuma publicação encontrada.")
    else:
        print("🔎 Resultados da busca:")
        for p in resultados:
            print("-", p)

# ---------------- CLI PRINCIPAL ----------------
def main():
    parser = argparse.ArgumentParser(prog="bib", description="Biblioteca Pessoal Digital")
    sub = parser.add_subparsers(dest="cmd")

    # cadastrar
    cad = sub.add_parser("cadastrar", help="Cadastrar uma publicação")
    cad.add_argument("--tipo", choices=["livro", "revista"], required=True)
    cad.add_argument("--titulo", required=True)
    cad.add_argument("--autor", required=True)
    cad.add_argument("--ano", type=int, required=True)
    cad.add_argument("--genero", required=True)
    cad.add_argument("--paginas", type=int, required=True)
    cad.add_argument("--isbn")
    cad.add_argument("--edicao", type=int)
    cad.set_defaults(func=cadastrar)

    # listar
    lst = sub.add_parser("listar", help="Listar publicações")
    lst.set_defaults(func=listar)

    # anotar
    ant = sub.add_parser("anotar", help="Adicionar anotação")
    ant.add_argument("--texto", required=True)
    ant.add_argument("--trecho")
    ant.set_defaults(func=anotar)

    # relatorio
    rel = sub.add_parser("relatorio", help="Gerar relatório")
    rel.set_defaults(func=relatorio)

    # buscar
    bsc = sub.add_parser("buscar", help="Buscar publicações")
    bsc.add_argument("--titulo")
    bsc.add_argument("--autor")
    bsc.add_argument("--genero")
    bsc.add_argument("--status", choices=["NÃO LIDO", "LENDO", "CONCLUIDO"])
    bsc.set_defaults(func=buscar)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


