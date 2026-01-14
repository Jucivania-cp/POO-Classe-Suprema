from statistics import mean

def top5_avaliacoes(publicacoes):
    avaliadas = [p for p in publicacoes if p.avaliacao is not None]
    return sorted(avaliadas, key=lambda p: p.avaliacao, reverse=True)[:5]

def medias(publicacoes):
    # média geral das avaliações e média por status
    avaliadas = [p.avaliacao for p in publicacoes if p.avaliacao is not None]
    media_geral = mean(avaliadas) if avaliadas else None

    por_status = {}
    for st in {"NAO_LIDO", "LENDO", "CONCLUIDO"}:
        vals = [p.avaliacao for p in publicacoes if p.status == st and p.avaliacao is not None]
        por_status[st] = mean(vals) if vals else None

    return {"geral": media_geral, "por_status": por_status}

def contagem_por_status(publicacoes):
    cont = {"NAO_LIDO": 0, "LENDO": 0, "CONCLUIDO": 0}
    for p in publicacoes:
        cont[p.status] += 1
    return cont
