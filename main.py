import numpy as np
import random
import matplotlib.pyplot as plt
import math

'''Declaração de constantes'''
size_populacao = 150
controle_crescimento_superior = 0.8
controle_crescimento_inferior = 0.4
taxa_de_mutacao = 0.05


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
    #   Cada individuo vai possuir uma sequência (caminho) e a distância de seu caminho
    def __init__(self, sequencia, distancia):
        self.sequencia = sequencia
        self.distancia = distancia


"""Função que cria aleatoriamente indivíduos para a primeira geração"""


def populacao_inicial():
    populacao = []

    for i in range(size_populacao):
        numeros = range(0, 9)
        gene = random.sample(numeros, 9)
        #   A primeira cidade sempre deve ser BSB (9)
        gene.insert(0, 9)
        dist = calcula_distancia(gene)
        populacao.append(Individuo(gene, dist))

        populacao = ordena_populacao(populacao)

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
    #   Necessário considerar a distância da última cidade para a primeira
    soma = soma + cidades[c][9]
    distancia = soma

    return distancia


'''Função que retorna vetor com índices ordenados por distâncias'''


def ordena_distancias(individuo):
    distancias = []
    for i in range(len(individuo)):
        distancias.append(individuo[i].distancia)
    distancias_ordenadas = np.argsort(distancias)
    return distancias_ordenadas


'''Função que ordena a populacao a partir do vetor gerado na função acima'''


def ordena_populacao(individuo):
    pop_ordenada = []
    ordem = ordena_distancias(individuo)
    for i in range(len(individuo)):
        gene = individuo[ordem[i]].sequencia
        dist = individuo[ordem[i]].distancia
        pop_ordenada.append(Individuo(gene, dist))
    return pop_ordenada


'''Função que retorna o individo com menor distância na população'''


def min_geracao(individuo):
    minimo = individuo[0].distancia
    gene = []
    for i in range(len(individuo)):
        if individuo[i].distancia < minimo:
            minimo = individuo[i].distancia
            gene = individuo[i].sequencia
    return Individuo(gene, minimo)


'''Probabilidade de reproducao'''


def reproduz(tamanho):
    if tamanho > size_populacao:
        return random.random() < controle_crescimento_inferior
    if tamanho <= 10:
        return True
    return random.random() < controle_crescimento_superior


'''Função para gerar filhos com reordenação aleatória dos cromossomos dos ancestrais'''


def procriacao_aleatoria(ancestral1, ancestral2):
    filho_gene1 = []

    gene1 = 1 + int(random.random() * len(ancestral1)-1)
    gene2 = 1 + int(random.random() * len(ancestral2)-1)

    inicio_gene = min(gene1, gene2)
    fim_gene = max(gene1, gene2)

    filho_gene1.append(9)
    for i in range(inicio_gene, fim_gene):
        filho_gene1.append(ancestral1[i])

    filho_gene2 = [item for item in ancestral2 if item not in filho_gene1]

    filho = filho_gene1 + filho_gene2
    return filho


"""Criação de uma nova geração a partir de combinações ordenadas da população ancestral"""


def cria_nova_geracao_procriacao_aleatoria(individuo):
    nova_geracao = []
    populacao_pequena = False
    if len(individuo) < 10:
        populacao_pequena = True
    #   Os 10% primeiros são os melhores candidatos e vão gerar novos filhos a partir do restante da populaçao
    k = int(size_populacao*0.1)
    if k == 0:
        k = 1

    for j in range(0, k):
        num_filhos = 0
        for i in range(k + 1, len(individuo)):

            # Caso o reprodutor já tenha atingido um limite superior de filhos
            # o laço é quebrado - isso garante que não ocorra super população
            if num_filhos >= int(10*math.exp(-size_populacao/1000)) and not populacao_pequena:
                break
            if reproduz(len(individuo)) or populacao_pequena:
                filho1 = procriacao_aleatoria(individuo[j].sequencia, individuo[i].sequencia)
                distancia_filho1 = calcula_distancia(filho1)
                filho1 = gera_mutacao(filho1)
                nova_geracao.append(Individuo(filho1, distancia_filho1))
                num_filhos = num_filhos + 1

            # Para garantir que a população não diminua, cada reprodutor tem a chance de fazer até 2 descendentes
            if reproduz(len(individuo)) or populacao_pequena:
                filho2 = procriacao_aleatoria(individuo[i].sequencia, individuo[j].sequencia)
                distancia_filho2 = calcula_distancia(filho2)
                filho2 = gera_mutacao(filho2)
                nova_geracao.append(Individuo(filho2, distancia_filho2))
                num_filhos = num_filhos + 1

        nova_geracao = ordena_populacao(nova_geracao)

    return nova_geracao


'''Função de aleatoriedade para mutação'''


def mutacao():
    return random.random() < taxa_de_mutacao


'''Funcao para gerar mutaçoes nos individuos'''


def gera_mutacao(individuo):
    if mutacao():
        posicao1 = 1 + int(random.random() * len(individuo) - 1)
        posicao2 = 1 + int(random.random() * len(individuo) - 1)
        gene1 = individuo[posicao1]
        gene2 = individuo[posicao2]
        individuo[posicao1] = gene2
        individuo[posicao2] = gene1

    return individuo


'''Funçao que roda o algoritmo genético com combinação aleatoria de genes'''


def roda_procriacao_aleatoria():
    geracao = populacao_inicial()
    vec_x = []
    vec_y = []
    plt.show()
    eixos = plt.gca()
    eixos.set_xlim(-10, 1000)
    eixos.set_ylim(100, 250)
    line, = eixos.plot(vec_x, vec_y, 'r-')
    plt.ylabel("Distância")
    plt.xlabel("Geração")
    plt.title("Procriação Aleatório")
    texto = str()
    minimo = min_geracao(geracao).distancia
    for i in range(0, 1000):
        geracao = cria_nova_geracao_procriacao_aleatoria(geracao)
        if min_geracao(geracao).distancia < minimo:
            minimo = min_geracao(geracao).distancia
            texto = "Geração: " + str(i) + "\nMínimo: " + str(minimo)
        # print("Geração: ", i, " - Tamanho: ", len(geracao))
        vec_x.append(i)
        vec_y.append(min_geracao(geracao).distancia)
        line.set_xdata(vec_x)
        line.set_ydata(vec_y)
        plt.draw()
    plt.text(600, 200, texto)
    return plt.show()


'''Função que faz a troca dos piores com os melhores pares e gera filhos'''


def reproducao_troca_duplas(ancestral1, ancestral2):
    filho_gene1 = []

    for i in range(0, 3):
        filho_gene1.append(ancestral1[i])

    filho_gene2 = [item for item in ancestral2 if item not in filho_gene1]

    filho = filho_gene1 + filho_gene2

    return filho


'''Função que cria nova geração com reprodução de troca de duplas'''


def gera_nova_geracao_troca_dupla(individuo):
    nova_geracao = []
    populacao_pequena = False
    if len(individuo) < 10:
        populacao_pequena = True
    #   Os 10% primeiros são os melhores candidatos e vão gerar novos filhos a partir do restante da populaçao
    k = int(size_populacao * 0.1)
    if k == 0:
        k = 1

    for j in range(0, k):
        num_filhos = 0
        for i in range(k + 1, len(individuo)):

            # Caso o reprodutor já tenha atingido um limite superior de filhos
            # o laço é quebrado - isso garante que não ocorra super população
            if num_filhos >= int(10 * math.exp(-size_populacao / 1000)) and not populacao_pequena:
                break
            if reproduz(len(individuo)) or populacao_pequena:
                filho1 = reproducao_troca_duplas(individuo[j].sequencia, individuo[i].sequencia)
                distancia_filho1 = calcula_distancia(filho1)
                filho1 = gera_mutacao(filho1)
                nova_geracao.append(Individuo(filho1, distancia_filho1))
                num_filhos = num_filhos + 1

            # Para garantir que a população não diminua, cada reprodutor tem a chance de fazer até 2 descendentes
            if reproduz(len(individuo)) or populacao_pequena:
                filho2 = reproducao_troca_duplas(individuo[i].sequencia, individuo[j].sequencia)
                distancia_filho2 = calcula_distancia(filho2)
                filho2 = gera_mutacao(filho2)
                nova_geracao.append(Individuo(filho2, distancia_filho2))
                num_filhos = num_filhos + 1

        nova_geracao = ordena_populacao(nova_geracao)

    return nova_geracao


'''Funçao que roda o algoritmo genético com combinação de pares'''


def roda_procriacao_troca_dupla():
    geracao = populacao_inicial()
    vec_x = []
    vec_y = []
    plt.show()
    eixos = plt.gca()
    eixos.set_xlim(-10, 1000)
    eixos.set_ylim(100, 250)
    line, = eixos.plot(vec_x, vec_y, 'r-')
    plt.ylabel("Distância")
    plt.xlabel("Geração")
    plt.title("Procriação por troca de pares")
    texto = str()
    minimo = min_geracao(geracao).distancia
    for i in range(0, 1000):
        geracao = gera_nova_geracao_troca_dupla(geracao)
        if min_geracao(geracao).distancia < minimo:
            minimo = min_geracao(geracao).distancia
            texto = "Geração: " + str(i) + "\nMínimo: " + str(minimo)
        vec_x.append(i)
        vec_y.append(min_geracao(geracao).distancia)
        line.set_xdata(vec_x)
        line.set_ydata(vec_y)
        plt.draw()
    plt.text(600, 200, texto)
    return plt.show()


def main():

    roda_procriacao_aleatoria()
    roda_procriacao_troca_dupla()


if __name__ == '__main__':
    main()
