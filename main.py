import math


# ======================== PARTE 1 ========================
def maximaAlturaTriangulo(N, B):
    # Array para altura máxima crescendo da esquerda para direita
    esquerda = [0] * N
    esquerda[0] = 1
    for i in range(1, N):
        esquerda[i] = min(esquerda[i - 1] + 1, B[i])

    # Array para altura máxima crescendo da direita para esquerda
    direita = [0] * N
    direita[N - 1] = 1
    for i in range(N - 2, -1, -1):
        direita[i] = min(direita[i + 1] + 1, B[i])

    # A altura máxima do triângulo é o mínimo entre esquerda e direita em cada posição
    alturaMaxima = 0
    for i in range(N):
        alturaMaxima = max(alturaMaxima, min(esquerda[i], direita[i]))

    return alturaMaxima


## ======================== PARTE 2 ========================


def getDistancia(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def calcPerimetro(p1, p2, p3):
    p = getDistancia(p1, p2) + getDistancia(p2, p3) + getDistancia(p1, p3)
    indices = tuple(sorted((p1[2], p2[2], p3[2])))
    return p, indices


def getMinPerimetro(p1, tri1, p2, tri2):
    if p1 < p2:
        return p1, tri1
    if p2 < p1:
        return p2, tri2

    # Desempate lexicográfico
    if tri1 is None:
        return p2, tri2
    if tri2 is None:
        return p1, tri1

    if tri1 < tri2:
        return p1, tri1
    else:
        return p2, tri2


# Função recursiva (divisão e conquista)
# Recebe px, uma tupla já ordenada por X
def encontrarMenorPerimetro(px):
    n = len(px)

    # Casos Base
    if n < 3:
        return math.inf, None

    if n == 3:
        return calcPerimetro(px[0], px[1], px[2])

    # Dividir
    indiceMeio = n // 2
    pxEsq = px[:indiceMeio]
    pxDir = px[indiceMeio:]

    # Linha vertical que divide o plano
    linhaMediaX = px[indiceMeio - 1][0]

    # Conquistar ---
    # Resolve recursivamente para a metade esquerda e direita
    (pEsq, triEsq) = encontrarMenorPerimetro(pxEsq)
    (pDir, triDir) = encontrarMenorPerimetro(pxDir)

    # Encontra o melhor resultado das duas metades (cuidando do desempate)
    (melhorP, melhorTri) = getMinPerimetro(pEsq, triEsq, pDir, triDir)

    # Combinar
    # Procura por um triângulo "cruzado" (com pontos em ambas as metades)
    # que seja melhor que o 'melhorP' atual.

    faixa = []
    # Filtra pontos que estão próximos da linha média
    # Um ponto só pode fazer parte de um triângulo melhor se estiver
    # a uma distância horizontal de 'melhorP / 2' da linha.
    for p in px:
        if abs(p[0] - linhaMediaX) < (melhorP / 2):
            faixa.append(p)

    # Ordena a faixa pela coordenada Y (essencial para otimização)
    faixa.sort(key=lambda p: p[1])

    # Procura na faixa por um trio melhor
    nFaixa = len(faixa)
    for i in range(nFaixa):
        for j in range(i + 1, nFaixa):
            # Otimização: Se a distância Y entre j e i já é muito grande,
            # podemos parar o loop interno 'j' (e 'k').
            if (faixa[j][1] - faixa[i][1]) >= (melhorP / 2):
                break

            for k in range(j + 1, nFaixa):
                # Otimização: Se a distância Y entre k e i é muito grande.
                if (faixa[k][1] - faixa[i][1]) >= (melhorP / 2):
                    break

                # Temos um triângulo candidato.
                (pAtual, triAtual) = calcPerimetro(faixa[i], faixa[j], faixa[k])

                # Atualiza o melhor resultado global
                (melhorP, melhorTri) = getMinPerimetro(
                    melhorP, melhorTri, pAtual, triAtual
                )

    return melhorP, melhorTri


numeroDePilhas = int(input())
quantidadePorPilha = list(map(int, input().split()))
numArvores = int(input())
listaPontos = []
for i in range(numArvores):
    x, y = map(int, input().split())
    # Armazena (x, y, indice_original)
    listaPontos.append((x, y, i + 1))

px = sorted(listaPontos, key=lambda p: p[0])

(perimetroFinal, triplaFinal) = encontrarMenorPerimetro(px)

print(f"Parte 1: {maximaAlturaTriangulo(numeroDePilhas, quantidadePorPilha)}")
print(
    f"Parte 2: {perimetroFinal:.4f} {triplaFinal[0]} {triplaFinal[1]} {triplaFinal[2]}"
)
