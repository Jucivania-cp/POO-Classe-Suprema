import argparse
from src.models.publicacao import Livro, Revista
from src.services.colecao import Colecao
from src.services.relatorios import top5_avaliacoes, medias, contagem_por_status
from src.persistence.repositorio import RepositorioJSON

def build_parser():
    parser = argparse.ArgumentParser(prog="bib", description="Biblioteca Pessoal Digital")
    sub = parser.add_subparsers(dest="comando")

    # CADASTRAR
    p = sub.add_parser("cadastrar", help="Cadastrar uma nova publicação")
    p.add_argument("--titulo", required=True)
    p.add_argument("--autor", required=True)
    p.add_argument("--ano", type=int, required=True)
    p.add_argument("--tipo", choices=["Livro", "Revista"], required=True)

    # LISTAR
    sub.add_parser("listar", help="Listar publicações")

    # STATUS
    si = sub.add_parser("iniciar", help="Marcar como LENDO")
    si.add_argument("--titulo", required=True)
    si.add_argument("--autor", required=True)
    si.add_argument("--ano", type=int, required=True)
    si.add_argument("--tipo", choices=["Livro", "Revista"], required=True)

    sc = sub.add_parser("concluir", help="Marcar como CONCLUIDO e opcionalmente avaliar")
    sc.add_argument("--titulo", required=True)
    sc.add_argument("--autor", required=True)
    sc.add_argument("--ano", type=int, required=True)
    sc.add_argument("--tipo", choices=["Livro", "Revista"], required=True)
    sc.add_argument("--avaliacao", type=int)

   
    # ANOTAR
    an = sub.add_parser("anotar", help="Adicionar anotação")
    an.add_argument("--titulo", required=True)
    an.add_argument("--autor", required=True)
    an.add_argument("--ano", type=int, required=True)
    an.add_argument("--tipo", choices=["Livro", "Revista"], required=True)
    an.add_argument("--texto", required=True)
    an.add_argument("--trecho")

    # RELATÓRIOS
    r = sub.add_parser("relatorios", help="Relatórios estatísticos")
    r.add_argument("--tipo", choices=["top5", "medias", "contagem"], required=True)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    repo = RepositorioJSON()
    colecao = Colecao(repo)

    try:
        if args.comando == "cadastrar":
            pub = Livro(args.titulo, args.autor, args.ano) if args.tipo == "Livro" else Revista(args.titulo, args.autor, args.ano)
            colecao.adicionar(pub)
            print(f"OK: '{args.titulo}' cadastrado.")
        elif args.comando == "listar":
            pubs = colecao.listar()
            for i, p in enumerate(pubs, 1):
                print(f"{i}. {p.tipo()} :: {p.titulo} - {p.autor} ({p.ano}) [{p.status}] "
                      f"{'(★ ' + str(p.avaliacao) + ')' if p.avaliacao is not None else ''}")
        elif args.comando == "iniciar":
            colecao.iniciar(args.titulo, args.autor, args.ano, args.tipo)
            print("OK: status atualizado para LENDO.")
        elif args.comando == "concluir":
            colecao.concluir(args.titulo, args.autor, args.ano, args.tipo, args.avaliacao)
            msg = "OK: status atualizado para CONCLUIDO."
            if args.avaliacao is not None:
                msg += f" Avaliação: {args.avaliacao}."
            print(msg)
        elif args.comando == "abandonar":
            colecao.abandonar(args.titulo, args.autor, args.ano, args.tipo)
            print("OK: status atualizado para ABANDONADO.")
        elif args.comando == "anotar":
            colecao.anotar(args.titulo, args.autor, args.ano, args.tipo, args.texto, args.trecho)
            print("OK: anotação adicionada.")
        elif args.comando == "relatorios":
            pubs = colecao.listar()
            if args.tipo == "top5":
                for i, p in enumerate(top5_avaliacoes(pubs), 1):
                    print(f"{i}. {p.titulo} - {p.autor} (★ {p.avaliacao})")
            elif args.tipo == "medias":
                m = medias(pubs)
                print(f"Média geral: {m['geral'] if m['geral'] is not None else '—'}")
                for st, val in m["por_status"].items():
                    print(f"{st}: {val if val is not None else '—'}")
            elif args.tipo == "contagem":
                c = contagem_por_status(pubs)
                for st, q in c.items():
                    print(f"{st}: {q}")
        else:
            parser.print_help()
    except ValueError as e:
        print(f"Erro: {e}")

