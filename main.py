import itertools
from shapely.geometry import LineString, Point
from tqdm import tqdm

def centro(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def episodio(n_episodios):
    A = (0, 0)
    B = (2, 0)
    C = (1, 2)

    M1 = centro(A, C)
    M2 = centro(B, C)

    nos = [A, B, C, M1, M2]  # 5 nós iniciais
    sequencia = [len(nos)]   # Guarda o número de nós por episódio

    for ep in range(n_episodios):
        novas_arestas = list(itertools.combinations(nos, 2))
        novos_nos = []

        combinacoes = list(itertools.combinations(novas_arestas, 2))
        loop = tqdm(combinacoes, desc=f"Episódio {ep+1}/{n_episodios} - Checando interseções", leave=False)

        for (p1, p2), (q1, q2) in loop:
            l1 = LineString([p1, p2])
            l2 = LineString([q1, q2])
            if l1.crosses(l2):
                intersecao = l1.intersection(l2)
                if isinstance(intersecao, Point):
                    ponto = (intersecao.x, intersecao.y)
                    if all(((ponto[0]-n[0])**2 + (ponto[1]-n[1])**2)**0.5 > 1e-6 for n in nos):
                        novos_nos.append(ponto)

        nos.extend(novos_nos)
        sequencia.append(len(nos))
        print(f"Episódio {ep+1}: {len(nos)} nós")

    return sequencia

n = 10
seq = episodio(n)
print("\nSequência de número de nós por episódio:")
for i, qtd in enumerate(seq):
    print(f"Episódio {i}: {qtd} nós")
