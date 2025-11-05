# Entrada: 1. número de pilhas
# 2. Número de blocos em cada pilha, em ordem crescente
# Saída: maior triângulo isosceles possível usandos os blocos, retirando os blocos que julgar desnecessário.
import math

def pilhasNecessarias(h):
    pilhas = 2 * h - 1
    return pilhas


pilhas = int(input())

blocos = [int(item) for item in input().split()]

# Sempre usar as pilhas mais altas primeiro
blocos.sort(reverse=True)

# Para construir um triângulo de altura H, precisamos de um total de (2*H − 1) pilhas
# Todas essas pilhas devem ter uma altura de pelo menos H
for h in range(1, len(blocos)+ 1):
    k = pilhasNecessarias(h)
    if (k > pilhas):
        break
    
    if (blocos[k - 1] >= h):
        continue
    else:
        # calcula e printa a altura
        altura = h - 1
        print("Parte 1:", altura)
        break