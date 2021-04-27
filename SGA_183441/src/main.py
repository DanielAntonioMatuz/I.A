import math
import random
from os import remove

import numpy as np
import matplotlib.pyplot as plt

# Parametros del sistema
N = 50  # Tamaño de la poblacion
valorCromosomaIndividuo = 4  # Valor de cromosomas por individo
generacionMaxima = 650  # Valor maximo de generaciones - iteraciones
pM = 100  # Probabilidad de Mutacion 1ra coordenada
# Variables del sistema
tamanioPoblacion = N + 1
tamanioGen = valorCromosomaIndividuo + 1
mejorIndividuoGen = 0
fitness = np.empty([tamanioPoblacion])  # fitness
# Probabilidad de cruza
Pc = np.empty([tamanioPoblacion])
arrayAuxPc = np.empty([tamanioPoblacion])
picosDatosGen = np.empty([generacionMaxima])

# Cromosomas
cromosoma = np.empty([tamanioPoblacion, tamanioGen], dtype=np.int)
nCromosoma = np.empty([tamanioPoblacion, tamanioGen], dtype=np.int)
H1 = np.empty([tamanioPoblacion, tamanioGen], dtype=np.int)
H2 = np.empty([tamanioPoblacion, tamanioGen], dtype=np.int)
# Guardar el mejor chromosoma
mejorGen = np.empty([generacionMaxima], dtype=np.int)
mejorIndividuoGen = 0
generacion = 0
datosTotales = list()



# Generar poblacion
def generarPoblacion():
    for i in range(1, tamanioPoblacion):
        for j in range(1, tamanioGen):
            # Random que permite generar los cromosomas aleatorias a los genes
            varAux = np.random.random_integers(100)
            varAux = varAux / 100
            if varAux <= 0.5:
                cromosoma[i, j] = 0
            else:
                cromosoma[i, j] = 1


# imprimir poblacion
def visualizarPoblacion():
    for i in range(1, tamanioPoblacion):
        for j in range(1, tamanioGen):
            print(cromosoma[i, j], end="")
        print()


# Evaluacion del fitness
def evaluacionFitness(generacion):
    i = 1
    j = 1
    valorCromosoma = ""
    fitness_total = 0
    promedioFitness = 0
    variance = 0
    for i in range(1, tamanioPoblacion):
        fitness[i] = 0

    for i in range(1, tamanioPoblacion):
        x = 0
        for j in range(1, tamanioGen):
            x = x + cromosoma[i, j] * pow(2, tamanioGen - j - 1)
        y = np.fabs((x - 1) / (3 + np.sin(x ** 2)))  # Ecuacion con solo valores absolutos  |EC: (x - 1) / ( 3 + Sen(x^2) )
        fitness[i] = y*10

        for k in range(1, tamanioGen):
            valorCromosoma += str(cromosoma[i, k])

        print("INDIVIDUO: ", i, " fitness = ", fitness[i]/10, "VALOR X en gráfica: ",fitness[i] , " valor de X: ", x, " CROMOSOMAS: ", valorCromosoma)
        valorCromosoma = ""
        fitness_total = fitness_total + fitness[i]
    promedioFitness = fitness_total / N
    # Realizar el calculo de la seleccion del mejor individuo
    individuoMejorGen = 0
    fitness_max = fitness[1]
    for i in range(1, tamanioPoblacion):
        if fitness[i] >= fitness_max:
            fitness_max = fitness[i]
            individuoMejorGen = i
    mejorGen[generacion] = individuoMejorGen
    # Obtenemos los resultados finales de todas las iteraciones para graficarlos
    f = open("output.txt", "a")
    f.write(str(generacion) + " " + str(fitness[mejorGen[generacion]]) + "\n")
    f.write(" \n")
    f.close()
    datosTotales.append(str(generacion) + " " + str(promedioFitness) + "\n")
    picosDatosGen[generacion] = fitness[mejorGen[generacion]]
    print("Tamaño de la población = ", tamanioPoblacion - 1)
    print("Individuo: [", mejorGen[generacion], "] con fitness (Aptitud) de mayor valor = ", fitness[mejorGen[generacion]])
    print("Sumatoria de fitness (Aptitud) total (Generación actual) = ", fitness_total)
    print("PROMEDIO FITNESS: ", promedioFitness)

#Seleccionar un turno aleatorio para elegir cruza
def seleccionarTurnoIndividuo():
    u1 = 0
    u2 = 0
    parent = 99
    while (u1 == 0 and u2 == 0):
        u1 = np.random.random_integers(tamanioPoblacion - 1)
        u2 = np.random.random_integers(tamanioPoblacion - 1)
        if fitness[u1] <= fitness[u2]:
            parent = u1
        else:
            parent = u2
    return parent


# Seleccion de Individuos para cruzar
def seleccionIndividuosCruza():
    fitness_total = 0
    parent = 0
    for i in range(1, tamanioPoblacion):
        fitness_total = fitness_total + fitness[i]
    for i in range(1, tamanioPoblacion):
        Pc[i] = fitness[i] / fitness_total #Proceso de seleccion de individuos para cruza a traves de ruleta
    for i in range(1, tamanioPoblacion):
        arrayAuxPc[0] = 0
    for i in range(1, tamanioPoblacion):
        arrayAuxPc[i] = arrayAuxPc[i - 1] + Pc[i] #Porcentaje acumulado
    u = np.random.uniform(0, 1)
    auxVal = 1
    k = 1
    while auxVal <= tamanioPoblacion - 1:
        for i in range(1, tamanioPoblacion): #Se generan las parejas verificando en que porcentaje cumplen
            if u < arrayAuxPc[i]:
                parent = i
                for j in range(1, tamanioGen):
                    nCromosoma[k, j] = cromosoma[parent, j]
                k = k + 1
                break
        u = np.random.uniform(0, 1)
        auxVal = auxVal + 1
    for i in range(1, tamanioPoblacion):
        for j in range(1, tamanioGen):
            cromosoma[i, j] = nCromosoma[i, j]


# Bloque para ejecutar la mutacion
# parMutacionPoblacion: Probabilidad de mutacion de la problación/individuo
# pMutacion: Probabilidad de que un cromosoma mute de un individuo
def procesoMutacion(parMutacionPoblacion, pMutacion):
    varAuxiliar = 0
    for i in range(1, tamanioPoblacion):
        up = np.random.random_integers(100)
        up = up / 100
        if up <= parMutacionPoblacion:
            for j in range(1, tamanioGen):
                varAuxiliar = np.random.random_integers(100) #Genera la probabilidad de quien individuo muta
                varAuxiliar = varAuxiliar / 100
                if varAuxiliar <= pMutacion:
                    if cromosoma[i, j] == 0:
                        nCromosoma[i, j] = 1
                    else:
                        nCromosoma[i, j] = 0
                else:
                    nCromosoma[i, j] = cromosoma[i, j]
        else:
            for j in range(1, tamanioGen):
                nCromosoma[i, j] = cromosoma[i, j]
    for i in range(1, tamanioPoblacion):
        for j in range(1, tamanioGen):
            cromosoma[i, j] = nCromosoma[i, j]


# Ejecucion del bloque de cruza:

def cruzamiento(probCruza):
    c = 1
    while (c <= N):
        procesoCruzamiento(probCruza)
        c = c + 1

def procesoCruzamiento(probCruza):
    j = 0
    puntoCruza = 0
    individuo1 = seleccionarTurnoIndividuo()
    individuo2 = seleccionarTurnoIndividuo()
    if random.random() <= probCruza:
        puntoCruza = np.random.random_integers(tamanioGen - 2)  # Punto de cruza | aleatorio
        # puntoCruza = 1
    j = 1
    while (j <= tamanioGen - 1):
        if j <= puntoCruza:
            H1[individuo1, j] = cromosoma[individuo1, j]
            H2[individuo2, j] = cromosoma[individuo2, j]

        else:
            H1[individuo1, j] = cromosoma[individuo2, j]
            H2[individuo2, j] = cromosoma[individuo1, j]
        j = j + 1

    j = 1
    for j in range(1, tamanioGen):
        cromosoma[individuo1, j] = H1[individuo1, j]
        cromosoma[individuo2, j] = H2[individuo2, j]

# Graficar los datos obtenidos
def graficarDatos():
    data = np.loadtxt('output.txt')
    remove("output.txt")
    x = data[:, 0]
    y = data[:, 1]
    plt.plot(x, y)
    plt.xlabel('Generación')
    plt.ylabel('Individuo con mejor FITNESS (Aptitud)')
    plt.xlim(0.0, 50.)
    plt.ylim(0.0, 650.)
    plt.show()


def procesoSGA():
    generacion = 0
    print("######################################### GENERACIÓN: ", generacion)
    print()
    generarPoblacion()
    visualizarPoblacion()
    evaluacionFitness(generacion)
    while (generacion < generacionMaxima - 1):
        print("Individuo con mejor fitnes de la generación: [", generacion, "] ", mejorGen[generacion])
        print()
        print("######################################### GENERACIÓN: ", generacion + 1)
        print()
        #Seleccionar individuos para realizar la cruza, actualizar la generación y calcular el fitness
        seleccionIndividuosCruza()
        generacion = generacion + 1
        evaluacionFitness(generacion)
        # Probabilidades de Cruza y mutación
        cruzamiento(0.75)  # Agregamos el valor de la probabilidad de la cruza
        procesoMutacion(0.01, 0.02)  # Agregamos el rango de la probabilidad de mutacion


if __name__ == '__main__':
    procesoSGA()
    graficarDatos()
    print("--------------------------------- PICOS DE DATOS TOTALES:")
    print(np.unique(picosDatosGen))