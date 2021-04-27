import math
import random
from os import remove
import copy
import numpy as np
import matplotlib.pyplot as plt

# PARAMETROS DE DISEÑO                                  #
N = 5  # Tamaño de la población
valorCromosomaIndividuo = 5  # Número de BITS para generar cromosomas de los individuos
generacionMaxima = 16  # Maximo valor de generaciones a iterar

# Variables del sistema                                #
popSize = N + 1
tamanioGen = valorCromosomaIndividuo + 1

mejorIndividuoGen = 0
# fitness
fitness = np.empty([popSize])

# probability
probability = np.empty([popSize])
net = np.empty([popSize])
# cromosomas
cromosomasIndividuo = np.empty([popSize, tamanioGen], dtype=np.int)
poblacionAnterior = np.empty([popSize, tamanioGen], dtype=np.int)
popAnterior = np.empty([popSize])
poblacionPODA = np.empty([popSize, tamanioGen], dtype=np.int)

ncromosomas = np.empty([popSize, tamanioGen], dtype=np.int)
H1 = np.empty([popSize, tamanioGen], dtype=np.int)
H2 = np.empty([popSize, tamanioGen], dtype=np.int)
# init and save best chromosome
mejorGen = np.empty([generacionMaxima], dtype=np.int)
mejorIndividuoGen = 0
GENERACION = 0



# INICIALIZAR PROBLACION                        #

def GenerarPoblacion():

    for i in range(1, popSize):
        for j in range(1, tamanioGen):
            varAuxGen = np.random.random_integers(100)
            varAuxGen = varAuxGen / 100
            if varAuxGen <= 0.5:
                cromosomasIndividuo[i, j] = 0
                poblacionPODA[i][j] = 0
            else:
                cromosomasIndividuo[i, j] = 1
                poblacionPODA[i][j] = 1



# VISUALIZAR POBLACION                                      #

def VisualizarPoblacion():
    varChromosoma = ""
    for i in range(1, popSize):
        x = 0
        for j in range(1, tamanioGen):
            print(cromosomasIndividuo[i, j], end="")
        print()
        for j in range(1, tamanioGen):
            x = x + cromosomasIndividuo[i, j] * pow(2, tamanioGen - j - 1)
        popAnterior[i] = int(x)


#########################################################
# EVALUACION DEL FITNESS                                    #
def EvualuacionFitnnes(generation):
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
        for j in range(1, tamanioGen):
            x = x + cromosomasIndividuo[i, j] * pow(2, tamanioGen - j - 1)
            y = np.fabs((x - 1) / (3 + np.sin(x ** 2)))  # Ecuacion con solo valores absolutos  |EC: (x - 1) / ( 3 + Sen(x^2) )

            fitness[i] = y * 100

        print("fitness = ", i, " ", fitness[i])
        fitness_total = fitness_total + fitness[i]
    fitness_average = fitness_total / N
    i = 1
    while i <= N:
        sum_sqr = sum_sqr + pow(fitness[i] - fitness_average, 2)
        i = i + 1
    variance = sum_sqr / N
    if variance <= 1.0e-4:
        variance = 0.0
    mejorGenSelect = 0
    fitness_max = fitness[1]
    for i in range(1, popSize):
        if fitness[i] >= fitness_max:
            fitness_max = fitness[i]
            mejorGenSelect = i
    mejorGen[generation] = mejorGenSelect
    f = open("output.txt", "a")
    f.write(str(generation) + " " + str(fitness_average) + "\n")
    f.write(" \n")
    f.close()
    print("Tamaño de la población = ", popSize - 1)
    print("Promedio Fitness de la población = ", fitness_average)
    print("Mejor Fitness = ", mejorGen[generation])


#########################################################
# Seleccionar un turno aleatorio para elegir cruza                       #
def SeleccionarTurno():
    u1 = 0
    u2 = 0
    parent = 99
    while (u1 == 0 and u2 == 0):
        u1 = np.random.random_integers(popSize - 1)
        u2 = np.random.random_integers(popSize - 1)
        if fitness[u1] <= fitness[u2]:
            parent = u1
        else:
            parent = u2
    return parent


#########################################################
# Seleccion de Individuos para cruzar                     #
def seleccionIndividuosCruza():
    fitness_total = 0
    parent = 0
    for i in range(1, popSize):
        fitness_total = fitness_total + fitness[i]
    for i in range(1, popSize):
        probability[i] = fitness[i] / fitness_total
    for i in range(1, popSize):
        net[0] = 0
    for i in range(1, popSize):
        net[i] = net[i - 1] + probability[i]
    u = np.random.uniform(0, 1)
    bugs = 1
    k = 1
    while bugs <= popSize - 1:
        for i in range(1, popSize):
            if u < net[i]:
                parent = i
                for j in range(1, tamanioGen):
                    ncromosomas[k, j] = cromosomasIndividuo[parent, j]
                k = k + 1
                break
        u = np.random.uniform(0, 1)
        bugs = bugs + 1
    for i in range(1, popSize):
        for j in range(1, tamanioGen):
            cromosomasIndividuo[i, j] = ncromosomas[i, j]
        #print("VALUE CROMO SELECT: ", chromosome[i])


#########################################################
# MUTACION POR BIT                           #
# pop_mutation_rate: Radio de porbabilidad de mutacion de la poblacion
# mutation_rate: Probabilidad de mutar por cada Bit
def mutation(pop_mutation_rate, mutation_rate):
    uallele = 0
    varnChromo = ""
    print(cromosomasIndividuo)
    for i in range(1, popSize):
        x = 0
        up = np.random.random_integers(100)
        up = up / 100
        if up <= pop_mutation_rate:
            for j in range(1, tamanioGen):
                uallele = np.random.random_integers(100)
                uallele = uallele / 100
                if uallele <= mutation_rate:
                    print("TRUE ==========")
                    if cromosomasIndividuo[i, j] == 0:
                        ncromosomas[i, j] = 1
                    else:
                        ncromosomas[i, j] = 0
                else:
                    ncromosomas[i, j] = cromosomasIndividuo[i, j]
        else:
            for j in range(1, tamanioGen):
                ncromosomas[i, j] = cromosomasIndividuo[i, j]

    #
    # poblacionPODA = np.append(popAnterior, poblacionEvaluando)
    # poblacionPODA = sorted(poblacionPODA)
    #
    # for i in range(int(((len(poblacionPODA) - 1) / 2) + 1), len(poblacionPODA) - 1):
    #     varAux = bin(int(poblacionPODA[i]))[2:]
    #     for j in range(1, tamanioGen):
    #         #print(varAux[j-1], " ", chromosome[i - N, j])
    #
    #         if int(cromosomasIndividuo[i - N, j]) < int(varAux[j - 1]):
    #             ncromosomas[i - N, j] = varAux[j - 1]
    #             cromosomasIndividuo[i - N, j] = ncromosomas[i - N, j]
    #
    #
    # for m in range(0, len(popAnterior)):
    #     popAnterior[m] = poblacionPODA[N + m]
    print(cromosomasIndividuo)

    poblacionPODA = copy.deepcopy(cromosomasIndividuo)

    #ACTUALIZAMOS LOS NUEVOS CROMOSOMAS PARA LA NUEVA GENERACION
    for i in range(1, popSize):
        for j in range(1, tamanioGen):
            cromosomasIndividuo[i, j] = ncromosomas[i, j]

    for i in range(1, popSize):
        print("POBLA ANT: ", i, " ", poblacionPODA[i])
        print("POBLA ACT: ", i, " ", cromosomasIndividuo[i])

    #
    #
    # for h in range(1, popSize):
    #     varX = 0
    #     varXR = 0
    #     for w in range(1, tamanioGen):
    #         varXR = varXR + poblacionAnterior[h, w] * pow(2, tamanioGen - w - 1)
    #     varX = np.fabs((varXR - 1) / (3 + np.sin(varXR ** 2)))
    #    # print("RESULTADO POP ANTERIOR: ", varX, " VALUE: ", varXR)
    #     for z in range(1, popSize):
    #         varY = 0
    #         varYR = 0
    #         for a in range(1, tamanioGen):
    #             varYR = varYR + cromosomasIndividuo[z, a] * pow(2, tamanioGen - a - 1)
    #         varY = np.fabs((varYR - 1) / (3 + np.sin(varYR ** 2)))
    #        # print("RESULTADO POP ACTUAL: ", varY, " VALUE: ", varYR)
    #         if varX > varY:
    #             print("POP ANTERIOR: ", varX, "VALUE: ", varXR, " POP ACTUAL: ", varY)
    #             # for k in range(1, tamanioGen):
    #             #     cromosomasIndividuo[z, k] = poblacionAnterior[z, k]
    #             print(cromosomasIndividuo[z])
    #             print(poblacionAnterior[z])
    #
    #                 #cromosomasIndividuo[z, u] = poblacionAnterior[z, u]
    #
    print(cromosomasIndividuo)
########################################################
# CRUZA DE UN PUNTO                                 #

def CrossingProcess(crossover_rate):
    j = 0
    crossover_point = 0
    padre1 = SeleccionarTurno()
    padre2 = SeleccionarTurno()
    if random.random() <= crossover_rate:
        crossover_point = np.random.random_integers(tamanioGen - 2)
    j = 1
    while (j <= tamanioGen - 1):
        if j <= crossover_point:
            H1[padre1, j] = cromosomasIndividuo[padre1, j]
            H2[padre2, j] = cromosomasIndividuo[padre2, j]

        else:
            H1[padre1, j] = cromosomasIndividuo[padre2, j]
            H2[padre2, j] = cromosomasIndividuo[padre1, j]
        j = j + 1

    j = 1
    for j in range(1, tamanioGen):
        cromosomasIndividuo[padre1, j] = H1[padre1, j]
        cromosomasIndividuo[padre2, j] = H2[padre2, j]


def crossover(crossover_rate):
    c = 1
    while (c <= N):
        CrossingProcess(crossover_rate)
        c = c + 1


def GenerarGrafico():
    data = np.loadtxt('output.txt')
    remove("output.txt")
    x = data[:, 0]
    y = data[:, 1]
    plt.plot(x, y)
    plt.xlabel('GENERACION')
    plt.ylabel('PROMEDIO FITNNES')
    plt.xlim(0.0, 15.)
    plt.ylim(0.0, 1300.)
    plt.show()



def IniciarSGA():
    generacion = 0
    print("============== GENERACION: ", generacion, " =========================== ")
    print()
    GenerarPoblacion()
    VisualizarPoblacion()
    EvualuacionFitnnes(generacion)
    while (generacion < generacionMaxima - 1):
        print("MEJOR GENERACIÓN [", generacion, "] ", mejorGen[generacion])
        print()
        print("============== GENERACION: ", generacion + 1, " =========================== ")
        print()
        seleccionIndividuosCruza()
        generacion = generacion + 1
        EvualuacionFitnnes(generacion)
        crossover(0.75)
        mutation(0.1, 0.22)


if __name__ == '__main__':
    IniciarSGA()
    GenerarGrafico()
