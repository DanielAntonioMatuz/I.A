import math
import random
from os import remove

import numpy as np
import matplotlib.pyplot as plt

N = 50  # Population size
Genome = 5  # Genome length
generation_max = 15  # Maximum of generations - iterations

popSize = N + 1
genomeLength = Genome + 1
# init best chromosome
the_best_chrom = 0
# fitness
fitness = np.empty([popSize])
# probability
probability = np.empty([popSize])
net = np.empty([popSize])
# chromosomes
chromosome = np.empty([popSize, genomeLength], dtype=np.int)
nchromosome = np.empty([popSize, genomeLength], dtype=np.int)
poblacionAnterior = np.empty([popSize, genomeLength], dtype=np.int)

child1 = np.empty([popSize, genomeLength], dtype=np.int)
child2 = np.empty([popSize, genomeLength], dtype=np.int)
# init and save best chromosome
best_chrom = np.empty([generation_max], dtype=np.int);
the_best_chrom = 0;
generation = 0;
GraphicAUX = []

def Init_population():
    for i in range(1, popSize):
        for j in range(1, genomeLength):
            allele = np.random.random_integers(100)
            allele = allele / 100
            if allele <= 0.5:
                chromosome[i, j] = 0
            else:
                chromosome[i, j] = 1


def Show_population():
    for i in range(1, popSize):
        for j in range(1, genomeLength):
            print(chromosome[i, j], end="")
        print()


def Fitness_evaluation(generation, chromosome):
    # fitness evaluation
    i = 1
    j = 1
    fitness_total = 0
    sum_sqr = 0
    fitness_average = 0
    variance = 0
    for i in range(1, popSize):
        fitness[i] = 0

    for i in range(1, popSize):
        x = 0
        for j in range(1, genomeLength):
            x = x + chromosome[i, j] * pow(2, genomeLength - j - 1)
            y = np.fabs((x - 1) / (3 + np.sin(x ** 2)))
            fitness[i] = y * 100

        print("fitness = ", i, " ", fitness[i])
        fitness_total = fitness_total + fitness[i]
    fitness_average = fitness_total / N
    i = 1;
    while i <= N:
        sum_sqr = sum_sqr + pow(fitness[i] - fitness_average, 2)
        i = i + 1
    variance = sum_sqr / N
    if variance <= 1.0e-4:
        variance = 0.0
    the_best_chrom = 0
    fitness_max = fitness[1]
    for i in range(1, popSize):
        if fitness[i] >= fitness_max:
            fitness_max = fitness[i]
            the_best_chrom = i
    best_chrom[generation] = the_best_chrom
    f = open("output.txt", "a")
    f.write(str(generation) + " " + str(fitness_average) + "\n")
    f.write(" \n")
    f.close()
    print("Tamanio poblacio = ", popSize - 1)
    print("Promedio fitness = ", fitness_average)
    print("fitness sum = ", fitness_total)


def select_p_tournament():
    u1 = 0;
    u2 = 0;
    parent = 99;
    while (u1 == 0 and u2 == 0):
        u1 = np.random.random_integers(popSize - 1)
        u2 = np.random.random_integers(popSize - 1)
        if fitness[u1] <= fitness[u2]:
            parent = u1
        else:
            parent = u2
    return parent


def wheel_p_selection():
    fitness_total = 0;
    parent = 0;
    for i in range(1, popSize):
        fitness_total = fitness_total + fitness[i]
    for i in range(1, popSize):
        probability[i] = fitness[i] / fitness_total
    for i in range(1, popSize):
        net[0] = 0
    for i in range(1, popSize):
        net[i] = net[i - 1] + probability[i]
    u = np.random.uniform(0, 1)
    bugs = 1;
    k = 1;
    while bugs <= popSize - 1:
        for i in range(1, popSize):
            if u < net[i]:
                parent = i
                for j in range(1, genomeLength):
                    nchromosome[k, j] = chromosome[parent, j]
                k = k + 1
                break
        u = np.random.uniform(0, 1)
        bugs = bugs + 1
    for i in range(1, popSize):
        for j in range(1, genomeLength):
            chromosome[i, j] = nchromosome[i, j]


def mutation(pop_mutation_rate, mutation_rate, generation):
    print("VALOR ORIGINAL =================: ")
    print(chromosome)
    uallele = 0
    for i in range(1, popSize):
        up = np.random.random_integers(100)
        up = up / 100
        if up <= pop_mutation_rate:
            for j in range(1, genomeLength):
                uallele = np.random.random_integers(100)
                uallele = uallele / 100
                if uallele <= mutation_rate:
                    print("TRUE ===============")
                    if chromosome[i, j] == 0:
                        nchromosome[i, j] = 1
                    else:
                        nchromosome[i, j] = 0
                else:
                    nchromosome[i, j] = chromosome[i, j]
        else:
            for j in range(1, genomeLength):
                nchromosome[i, j] = chromosome[i, j]

    print("==================================")
    AuxPoblation = []

    print(chromosome)
    print("==================================")

    for i in range(1, popSize):
        auxList = []
        for j in range(1, genomeLength):
            auxList.append(chromosome[i, j])
        AuxPoblation.append(auxList)

    for k in range(1, popSize):
        auxList2 = []
        for a in range(1, genomeLength):
            auxList2.append(nchromosome[k, a])
        AuxPoblation.append(auxList2)

    #print(AuxPoblation)
    ReorderPopFitness = [(valueFitnessPoblationIndividual(i), i) for i in AuxPoblation]
    print(ReorderPopFitness)
    ReorderPopFitness = [i[1] for i in sorted(ReorderPopFitness)]

    AuxListPop = ReorderPopFitness[(len(ReorderPopFitness)-N) : ]

    print("=================== ANTES: ")
    print(AuxListPop)
    GraphicAUX.append(AuxListPop)

    print("=================== RESULTADO: ")
    for i in range(1, popSize):
         for j in range(1, genomeLength):
             chromosome[i, j] = AuxListPop[i-1][j-1]
    print(chromosome)
    Fitness_evaluation(generation, chromosome)


def valueFitnessPoblationIndividual(pop_value):
    #print("POP VALUE: ", pop_value)
    varYR = 0
    for a in range(0, len(pop_value)):
         varYR = varYR + pop_value[a] * pow(2, len(pop_value) - a -1)
    #print("VALOR X: ", varYR)
    result_fitness = np.fabs((varYR - 1) / (3 + np.sin(varYR ** 2)))
    return result_fitness



def mating(crossover_rate):
    j = 0
    crossover_point = 0;
    parent1 = select_p_tournament()
    parent2 = select_p_tournament()
    if random.random() <= crossover_rate:
        crossover_point = np.random.random_integers(genomeLength - 2)
    j = 1
    while (j <= genomeLength - 1):
        if j <= crossover_point:
            child1[parent1, j] = chromosome[parent1, j]
            child2[parent2, j] = chromosome[parent2, j]

        else:
            child1[parent1, j] = chromosome[parent2, j]
            child2[parent2, j] = chromosome[parent1, j]
        j = j + 1

    j = 1
    for j in range(1, genomeLength):
        chromosome[parent1, j] = child1[parent1, j]
        chromosome[parent2, j] = child2[parent2, j]


def crossover(crossover_rate):
    c = 1
    while (c <= N):
        mating(crossover_rate)
        c = c + 1


def plot_Output():
    data = np.loadtxt('output.txt')
    remove("output.txt")
    x = data[:, 0]
    y = data[:, 1]
    plt.plot(x, y)
    plt.xlabel('Generation')
    plt.ylabel('Fitness average')
    plt.xlim(0.0, 15.)
    plt.ylim(0.0, 2000.)
    print(GraphicAUX)
    plt.show()


def Simple_GA():
    generation = 0
    print("============== GENERATION: ", generation, " =========================== ")
    print()
    Init_population()
    Show_population()
    while (generation < generation_max - 1):
        print("Mejor generacion [", generation, "] ", best_chrom[generation])
        print()
        print("============== GENERATION: ", generation + 1, " =========================== ")
        print()
        wheel_p_selection()
        generation = generation + 1

        crossover(0.75)
        mutation(0.1, 0.2, generation)



if __name__ == '__main__':
    Simple_GA()
    plot_Output()
    for i in range(0, len(GraphicAUX)):
        for j in range(0, 5):
            print(valueFitnessPoblationIndividual(GraphicAUX[i][j]))