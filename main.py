import numpy as np
import random


size_populacao = 3


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


class Individuo:
    def __init__(self, sequencia, distancia):
        self.sequencia = sequencia
        self.distancia = distancia


"""Função que cria aleatoriamente indivíduos para a primeira geração"""


def populacao_inicial():
    populacao = []

    for i in range(size_populacao):
        numeros = range(0, 9)
        gene = random.sample(numeros, 9)
        gene.insert(0, 9)
        dist = calcula_distancia(gene)
        populacao.append(Individuo(gene, dist))

    return populacao


"""Função que calcula a distância total percorrida por cada individuo"""


def calcula_distancia(gene):
    soma = 0
    i = 0
    for i in range(9):
        a = int(gene[i])
        b = int(gene[i+1])
        soma = soma + cidades[a][b]
    c = int(gene[i-1])
    soma = soma + cidades[c][9]
    distancia = soma

    return distancia


""""Funão que recolhe a menor distância daquela população"""


def min_geracao(individuo):
    minimo = individuo[0].distancia
    for i in range(size_populacao):
        if individuo[i].distancia < minimo:
            minimo = individuo[i].distancia
    return minimo


"""Função que calcula a distância média das novas gerações"""


def media_geracao(individuo):
    media = 0
    for i in range(size_populacao):
        media = media + individuo[i].distancia
    media = media/size_populacao
    return int(media)


def main():

    populacao = populacao_inicial()
    for i in range(size_populacao):
        print(populacao[i].sequencia, " --- ", populacao[i].distancia)

    print("Individuo mais proximo do objetivo: ", min_geracao(populacao))
    print("Media da populacao: ", media_geracao(populacao))


if __name__ == '__main__':
    main()
