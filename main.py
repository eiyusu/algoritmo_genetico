import numpy as np
import random


size_populacao = 100


"""Matriz com as distâncias das cidades

   Cidade 0: SP       |     Cidade 5: Sant.
   Cidade 1: BA       |     Cidade 6: Carac.
   Cidade 2: RJ       |     Cidade 7: BH
   Cidade 3: Lima     |     Cidade 8: PoA
   Cidade 4: Bog.     |     Cidade 9: BSB
"""
cidades = np.array([[0, 17, 3, 35, 43, 26, 44, 5, 8, 9], [17, 0, 20, 31, 47, 11, 51, 22, 8, 23],
                    [3, 20, 0, 38, 45, 29, 45, 3, 11, 9], [35, 31, 38, 0, 19, 25, 27, 36, 33, 32],
                    [43, 47, 45, 19, 0, 43, 10, 43, 46, 37], [26, 11, 29, 25, 43, 0, 49, 30, 19, 30],
                    [44, 51, 45, 27, 10, 49, 0, 42, 48, 35], [5, 22, 3, 36, 43, 30, 42, 0, 13, 6],
                    [8, 8, 11, 33, 46, 19, 48, 13, 0, 16], [9, 23, 9, 32, 37, 30, 35, 6, 16, 0]])


"""Função que cria aleatoriamente indivíduos para a primeira geração"""


def populacao_inicial():
    populacao = np.zeros((size_populacao, 10))

    for i in range(size_populacao):
        numeros = range(0, 9)
        individuo = random.sample(numeros, 9)
        individuo.insert(0, 9)
        populacao[i] = individuo

    return populacao


"""Função que calcula a distância total percorrida por cada individuo"""


def calcula_distancia(individuo):
    distancias = np.zeros(size_populacao)
    for k in range(size_populacao):
        soma = 0
        i = 0
        for i in range(9):
            a = int(individuo[k][i])
            b = int(individuo[k][i+1])
            soma = soma + cidades[a][b]
        c = int(individuo[k][i-1])
        soma = soma + cidades[c][9]
        distancias[k] = soma

    return distancias


""""Funão que recolhe a menor distância daquela população"""


def min_geracao(distancias):
    minimo = distancias[0]
    for i in range(size_populacao):
        if distancias[i] < minimo:
            minimo = distancias[i]
    return minimo


"""Função que calcula a distância média das novas gerações"""


def media_geracao(distancias):
    media = 0
    for i in range(size_populacao):
        media = media + distancias[i]
    media = media/size_populacao
    return int(media)


def main():

    populacao = populacao_inicial()
    print(populacao)
    distancias = calcula_distancia(populacao)
    print(distancias)
    minimo = min_geracao(distancias)
    print(minimo)
    media = media_geracao(distancias)
    print(media)


if __name__ == '__main__':
    main()
