import argparse
from src.models import Livro, Revista, Anotacao
from src.persistence.repositorio import RepositorioJSON
from src.services.colecao import Colecao

repo = RepositorioJSON("data/biblioteca.json")
colecao = Colecao(repo)

# ---------------- COMANDOS ----------------

def cadastrar(args):
    pub = None
    if args.tipo == "livro":
        if args.edicao is not None:
            print("ATENÇÃO: Para livros, não use --edicao.")
            return
        pub = Livro(args.titulo, args.autor, args.ano, args.genero, args.paginas, args.isbn)

    elif args.tipo == "revista":
        if args.isbn is not None:
            print("ATENÇÃO: Revista não aceita --isbn.")
            return
        pub = Revista(args.titulo, args.autor, args.ano, args.genero, args.paginas, args.edicao)

    else:
        print("ATENÇÃO: Tipo inválido.")
        return

    # só chega aqui se pub foi criado
    try:
        colecao.adicionar(pub)
        print("Publicação cadastrada:", pub)
    except Exception as e:
        print("Erro ao cadastrar:", e)


def listar(args):
    pubs = colecao.listar()
    if not pubs:
        print("Nenhuma publicação cadastrada.")
    else:
        for i, p in enumerate(pubs):
            print(f"[{i}] {p}")

def iniciar(args):
    pubs = colecao.listar()
    try:
        pub = pubs[args.index]
        pub.iniciar_leitura()
        colecao.repositorio.salvar(colecao.publicacoes)
        print("Leitura iniciada:", pub)
    except Exception as e:
        print("Erro:", e)

def concluir(args):
    pubs = colecao.listar()
    try:
        pub = pubs[args.index]
        pub.concluir_leitura()
        colecao.repositorio.salvar(colecao.publicacoes)
        print("Leitura concluída:", pub)
    except Exception as e:
        print("Erro:", e)

def anotar(args):
    pubs = colecao.listar()
    try:
        pub = pubs[args.index]
        anot = Anotacao(args.texto)
        pub.adicionar_anotacao(anot)
        colecao.repositorio.salvar(colecao.publicacoes)
        print(f"Anotação adicionada em '{pub.titulo}': {args.texto}")
    except Exception as e:
        print("Erro:", e)


def buscar_titulo(args):
    pubs = [p for p in colecao.listar() if args.titulo.lower() in p.titulo.lower()]
    if not pubs:
        print("Nenhum resultado para título:", args.titulo)
    else:
        for p in pubs:
            print("-", p)

def buscar_autor(args):
    pubs = [p for p in colecao.listar() if args.autor.lower() in p.autor.lower()]
    if not pubs:
        print("Nenhum resultado para autor:", args.autor)
    else:
        for p in pubs:
            print("-", p)

def avaliar(args):
    pubs = colecao.listar()
    try:
        pub = pubs[args.index]
        pub.avaliacao = args.nota
        colecao.repositorio.salvar(colecao.publicacoes)
        print(f"Avaliação registrada para '{pub.titulo}': {pub.avaliacao}")
    except Exception as e:
        print("Erro:", e)


def remover(args):
    pubs = colecao.listar()
    try:
        pub = pubs[args.index]
        colecao.remover(pub)
        print("Publicação removida:", pub)
    except Exception as e:
        print("Erro:", e)

# ---------------- MAIN ----------------

def main():
    parser = argparse.ArgumentParser(prog="bib", description="Biblioteca Pessoal Digital")
    sub = parser.add_subparsers(dest="cmd")

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

    lst = sub.add_parser("listar", help="Listar publicações")
    lst.set_defaults(func=listar)

    ini = sub.add_parser("iniciar", help="Iniciar leitura")
    ini.add_argument("--index", type=int, required=True)
    ini.set_defaults(func=iniciar)

    con = sub.add_parser("concluir", help="Concluir leitura")
    con.add_argument("--index", type=int, required=True)
    con.set_defaults(func=concluir)

    an = sub.add_parser("anotar", help="Adicionar anotação a uma publicação")
    an.add_argument("--index", type=int, help="Índice da publicação")
    an.add_argument("--texto", help="Texto da anotação")
    an.set_defaults(func=anotar)

    bt = sub.add_parser("buscar-titulo", help="Buscar por título")
    bt.add_argument("--titulo", required=True)
    bt.set_defaults(func=buscar_titulo)

    ba = sub.add_parser("buscar-autor", help="Buscar por autor")
    ba.add_argument("--autor", required=True)
    ba.set_defaults(func=buscar_autor)

    av = sub.add_parser("avaliar", help="Avaliar uma publicação concluída")
    av.add_argument("--index", type=int, required=True, help="Índice da publicação na lista")
    av.add_argument("--nota", type=float, required=True, help="Nota de 0 a 10")
    av.set_defaults(func=avaliar)

    rm = sub.add_parser("remover", help="Remover publicação")
    rm.add_argument("--index", type=int, required=True)
    rm.set_defaults(func=remover)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
