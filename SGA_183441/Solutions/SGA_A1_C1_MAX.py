import math
import random
from os import remove

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import *


# VAR_EXT = np.ones([1])
#
# window = Tk()
# window.title("Bienvenido al SGA - Maximizar")
# ancho_ventana = 320
# alto_ventana = 100
# x_ventana = window.winfo_screenwidth() // 2 - ancho_ventana // 2
# y_ventana = window.winfo_screenheight() // 2 - alto_ventana // 2
# posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
# window.geometry(posicion)
#
# lbl = Label(window, text="Ingrese el valor de la población: ")
# lbl.grid(column=0, row=0)
#
# txt = Entry(window, width=10)
# txt.grid(column=1, row=0)
#
#
# def clicked():
#     N = int(txt.get())
#     if N == 0:
#         N = 50
#
#     print("N: ", N)
#     VAR_EXT[0] = N
#     return N
#
#
# btn = Button(window, text="ACEPTAR", command=clicked)
# btn.grid(column=2, row=0)
# window.mainloop()

# TIPO: MAXIMIZAR

N = 70  # Tamaño de la población
bits_gen = 8  # Valor de bits que tendra cada individuo (cromosomas)
generaciones = 50  # Maximo numero de generaciones - iteraciones
# Variables de configuracion del sistema multivariable
numberVariablesEc = 3
particiones = np.empty([numberVariablesEc + 1])
popSize = N + 1
gen_tamanio = (bits_gen * numberVariablesEc) + 1
mejor_gen_individuo = 0

fitness = np.empty([popSize])
probability = np.empty([popSize])
net = np.empty([popSize])

cromosoma_poblacion = np.zeros([popSize, gen_tamanio], dtype=np.int)
cromosoma_poblacion_peor = np.zeros([popSize, gen_tamanio], dtype=np.int)
n_cromosoma_poblacion = np.zeros([popSize, gen_tamanio], dtype=np.int)
poblacionAnterior = np.zeros([popSize, gen_tamanio], dtype=np.int)
H1 = np.zeros([popSize, gen_tamanio], dtype=np.int)
H2 = np.zeros([popSize, gen_tamanio], dtype=np.int)
mejor_individuo_pop = np.empty([generaciones], dtype=np.int)
mejor_gen_individuo = 0
generacion = 0
GraphicAUX = []


def Generar_Poblacion():
    for i in range(1, popSize):
        for j in range(1, gen_tamanio):
            varAux = random.randint(1, 100 + 1)
            varAux = varAux / 100
            if varAux <= 0.5:
                cromosoma_poblacion[i, j] = 0
            else:
                cromosoma_poblacion[i, j] = 1


def Visualizar_poblacion():
    for i in range(1, popSize):
        for j in range(1, gen_tamanio):
            print(cromosoma_poblacion[i, j], end="")
        print()


def Fitness_evaluation(generation, chromosome):
    i = 1
    j = 1
    fitness_total = 0
    fitness_average = 0
    for i in range(1, popSize):
        fitness[i] = 0

    for i in range(1, popSize):
        x = 0
        y = 0
        z = 0
        for j in range(1, gen_tamanio):
            for g in range(1, 9):
                x = x + chromosome[i, g] * pow(2, 8 - g - 1)

            for v in range(9, 17):
                y = y + chromosome[i, v] * pow(2, 17 - v - 1)

            for t in range(17, 25):
                z = z + chromosome[i, t] * pow(2, 25 - t - 1)

            R = np.fabs(np.sin(x ** 2) + (3 * (y ** 3)) - (4 * z))
            fitness[i] = R / 1000
            # print("X: ", x, " Y: ", y, " Z: ", z, " FITNESS: ", R)
            x = 0
            y = 0
            z = 0

        print("fitness = ", i, " ", fitness[i])
        fitness_total = fitness_total + fitness[i]
    fitness_average = fitness_total / N

    the_best_chrom = 0
    fitness_max = fitness[1]
    for i in range(1, popSize):
        if fitness[i] >= fitness_max:
            fitness_max = fitness[i]
            the_best_chrom = i
    mejor_individuo_pop[generation] = the_best_chrom
    f = open("output.txt", "a")
    f.write(str(generation) + " " + str(fitness_average) + "\n")
    f.write(" \n")
    f.close()
    print("Tamaño de la población = ", popSize - 1)
    print("Promedio Fitness: = ", fitness_average)
    print("Mejor fitness = ", mejor_individuo_pop[generation])
    print("Sumatoria Fitness de la población actual = ", fitness_total)


def seleccion_p_cruza():
    u1 = 0
    u2 = 0
    AuxVar = 99
    while (u1 == 0 and u2 == 0):
        u1 = random.randint(0, popSize - 1)
        u2 = random.randint(0, popSize - 1)
        if fitness[u1] <= fitness[u2]:
            AuxVar = u1
        else:
            AuxVar = u2
    return AuxVar


def origanizacion_ruleta():
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
                for j in range(1, gen_tamanio):
                    n_cromosoma_poblacion[k, j] = cromosoma_poblacion[parent, j]
                k = k + 1
                break
        u = np.random.uniform(0, 1)
        bugs = bugs + 1
    for i in range(1, popSize):
        for j in range(1, gen_tamanio):
            cromosoma_poblacion[i, j] = n_cromosoma_poblacion[i, j]


def Proceso_mutacion(Pm_pop, Pm, generation):
    varAuxMut = 0
    for i in range(1, popSize):
        up = np.random.random_integers(100)
        up = up / 100
        if up <= Pm_pop:
            for j in range(1, gen_tamanio):
                varAuxMut = np.random.random_integers(100)
                varAuxMut = varAuxMut / 100
                if varAuxMut <= Pm:
                    if cromosoma_poblacion[i, j] == 0:
                        n_cromosoma_poblacion[i, j] = 1
                    else:
                        n_cromosoma_poblacion[i, j] = 0
                else:
                    n_cromosoma_poblacion[i, j] = cromosoma_poblacion[i, j]
        else:
            for j in range(1, gen_tamanio):
                n_cromosoma_poblacion[i, j] = cromosoma_poblacion[i, j]
    AuxPoblation = []

    for i in range(1, popSize):
        auxList = []
        for j in range(1, gen_tamanio):
            auxList.append(cromosoma_poblacion[i, j])
        AuxPoblation.append(auxList)

    for k in range(1, popSize):
        auxList2 = []
        for a in range(1, gen_tamanio):
            auxList2.append(n_cromosoma_poblacion[k, a])
        AuxPoblation.append(auxList2)

    ReorderPopFitness = [(valueFitnessPoblationIndividual(i), i) for i in AuxPoblation]
    ReorderPopFitness = [i[1] for i in sorted(ReorderPopFitness)]


    AuxListPop = ReorderPopFitness[(len(ReorderPopFitness) - N):]
    AuxListPeorPop = ReorderPopFitness[0: N]

    GraphicAUX.append(AuxListPop)

    for i in range(1, popSize):
        for j in range(1, gen_tamanio):
            cromosoma_poblacion[i, j] = AuxListPop[i - 1][j - 1]

    sum_fitness_low = 0
    #cromosoma_poblacion_peor

    for w in range(1, popSize):
        for p in range(1, gen_tamanio):
            cromosoma_poblacion_peor[w, p] = AuxListPeorPop[w - 1][p - 1]

    for h in range(1, popSize):
        sum_fitness_low += valueFitnessPoblationIndividual(cromosoma_poblacion_peor[h])

    sum_fitness_low = sum_fitness_low/N

    f = open("output2.txt", "a")
    f.write(str(generation) + " " + str(sum_fitness_low-1000) + "\n")
    f.write(" \n")
    f.close()

    Fitness_evaluation(generation, cromosoma_poblacion)


def valueFitnessPoblationIndividual(pop_value):
    x = 0
    y = 0
    z = 0
    for g in range(0, 8):
        x = x + pop_value[g] * pow(2, 8 - g - 1)

    for v in range(8, 16):
        y = y + pop_value[v] * pow(2, 16 - v - 1)

    for t in range(16, 23):
        z = z + pop_value[t] * pow(2, 23 - t - 1)

    result_fitness = np.fabs(np.sin(x ** 2) + (3 * (y ** 3)) - (4 * z))
    result_fitness = result_fitness / 1000
    return result_fitness


def Proceso_cruza(Pc):
    j = 0
    punto_cruza = 0
    padre1 = seleccion_p_cruza()
    padre2 = seleccion_p_cruza()

    if random.random() <= Pc:
        punto_cruza = random.randint(0, gen_tamanio - 2)
    j = 1
    while (j <= gen_tamanio - 1):
        if j <= punto_cruza:
            H1[padre1, j] = cromosoma_poblacion[padre1, j]
            H2[padre2, j] = cromosoma_poblacion[padre2, j]

        else:
            H1[padre1, j] = cromosoma_poblacion[padre2, j]
            H2[padre2, j] = cromosoma_poblacion[padre1, j]
        j = j + 1

    j = 1
    for j in range(1, gen_tamanio):
        cromosoma_poblacion[padre1, j] = H1[padre1, j]
        cromosoma_poblacion[padre2, j] = H2[padre2, j]


def Cruza(Pc):
    c = 1
    while (c <= N):
        Proceso_cruza(Pc)
        c = c + 1


def Graficar():
    data = np.loadtxt('output.txt')
    remove("output.txt")

    dataLow = np.loadtxt('output2.txt')
    remove("output2.txt")

    x = data[:, 0]
    y = data[:, 1]
    z = dataLow[:, 1]
    plt.title("Evolución del fitness (MAXIMIZAR)")
    # plt.plot(x, y)
    plt.plot(x, y, color="green", label="Mejor Fitness")
    plt.plot(sorted(z), color="red", label="Peor Fitness")
    plt.xlabel('GENERACION')
    plt.ylabel('PROMEDIO FITNESS')
    plt.legend()
    plt.show()


def IniciarSGA():
    generation = 0
    print("============== GENERACION: ", generation, " =========================== ")
    print()
    Generar_Poblacion()
    Visualizar_poblacion()
    while (generation < generaciones - 1):
        print("Mejor generacion: [", generation, "] | mejor individuo: ", mejor_individuo_pop[generation])
        print()
        print("============== GENERACION: ", generation + 1, " =========================== ")
        print()
        origanizacion_ruleta()
        generation = generation + 1
        Cruza(0.75)
        Proceso_mutacion(0.1, 0.08, generation)


if __name__ == '__main__':
    IniciarSGA()
    Graficar()
