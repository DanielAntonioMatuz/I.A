import random

import matplotlib
import matplotlib.pyplot as plt

globalListX = list()
globalListFX = list()
globalListCromosoma = list()
globalPercentege = list()
globalPercentegeUpdate = list()
globalGeneratedIndividuals = list()
globalSeleccionCruza = list()
auxSeleccionCruza = list()
probabilityCrossing = 0.8
probabilityMutation = 0.26
finalResults = list()
poblacionInicial = list()
firstAccess = True
iteration = 0

def restartFunction():
    del globalListX[:]
    del globalListFX[:]
    del globalListCromosoma[:]
    del globalPercentege[:]
    del globalPercentegeUpdate[:]
    del globalGeneratedIndividuals[:]
    del globalSeleccionCruza[:]
    del auxSeleccionCruza[:]
    del poblacionInicial[:]

def executeMutation():
    mutationList = []
    val1 = ""
    val2 = ""
    val3 = ""
    numero_decimal_1 = 0
    numero_decimal_2 = 0
    numero_decimal_3 = 0

    print("Mutation Process")


    for i in range(0, len(globalSeleccionCruza)):
        aux = []
        for j in range(0,len(globalListCromosoma[i])):
            aux.append(random.randrange(0, 100))
        mutationList.append([aux])
    print(mutationList)
    print(globalSeleccionCruza)

    for k in range(0, len(globalSeleccionCruza)):
        for j in range(0, len(mutationList[k][0])):
            if ((mutationList[k][0][j]/100) <= probabilityMutation):
                if int(globalSeleccionCruza[k][3][j]) == 1:
                    globalSeleccionCruza[k][3][j] = 0
                else:
                    globalSeleccionCruza[k][3][j] = 1

        finalResults.append(globalSeleccionCruza[k])

    for kj in range(0, 5):
        val1 = val1 + str(globalSeleccionCruza[0][3][kj])
    for ij in range(0, 5):
        val2 = val2 + str(globalSeleccionCruza[1][3][ij])
    for ix in range(0, 5):
        val3 = val3 + str(globalSeleccionCruza[2][3][ix])


    for posicion, digito_string in enumerate(val1[::-1]):
        numero_decimal_1 += int(digito_string) * 2 ** posicion

    for posicion, digito_string in enumerate(val2[::-1]):
        numero_decimal_2 += int(digito_string) * 2 ** posicion

    for posicion, digito_string in enumerate(val3[::-1]):
        numero_decimal_3 += int(digito_string) * 2 ** posicion

    globalSeleccionCruza[0][1] = numero_decimal_1
    globalSeleccionCruza[0][2] = functionMath(numero_decimal_1)

    globalSeleccionCruza[1][1] = numero_decimal_2
    globalSeleccionCruza[1][2] = functionMath(numero_decimal_2)

    globalSeleccionCruza[2][1] = numero_decimal_3
    globalSeleccionCruza[2][2] = functionMath(numero_decimal_3)

    restartFunction()

    print(finalResults) #Aqui se almacena el resultado final con mutacion aplicada, listo para graficar
    print("FINAL")


    poblacionInicial = finalResults
    print(poblacionInicial)
    firstAccess = False

    if iteration == 2:
        auxList = []

        for ijk in range(0, len(poblacionInicial)):
            auxList.append(poblacionInicial[ijk][1])

        plt.plot(auxList)
        plt.xlabel('Generation')
        plt.ylabel('Best score (% target)')
        plt.show()

    print(poblacionInicial)







def executeCrossing():

    listAux = []
    val1 = ""
    val2 = ""
    numero_decimal_1 = 0
    numero_decimal_2 = 0

    for jx in range(0, len(globalSeleccionCruza[2][3])):
        auxSeleccionCruza.append(globalSeleccionCruza[2][3][jx])

    for j in range(0, len(globalSeleccionCruza[1][3])):
        listAux.append(globalSeleccionCruza[1][3][j])


    for k in range(2,5):
        globalSeleccionCruza[1][0] = "H2"
        globalSeleccionCruza[1][3][k] = globalSeleccionCruza[0][3][k]



    for i in range(2,5):
        globalSeleccionCruza[0][0] = "H1"
        globalSeleccionCruza[0][3][i] = listAux[i]

    for kj in range(0, 5):
        val1 = val1 + globalSeleccionCruza[0][3][kj]
    for ij in range(0, 5):
        val2 = val2 + globalSeleccionCruza[1][3][ij]


    for posicion, digito_string in enumerate(val1[::-1]):
        numero_decimal_1 += int(digito_string) * 2 ** posicion

    for posicion, digito_string in enumerate(val2[::-1]):
        numero_decimal_2 += int(digito_string) * 2 ** posicion

    globalSeleccionCruza[0][1] = numero_decimal_1
    globalSeleccionCruza[0][2] = functionMath(numero_decimal_1)

    globalSeleccionCruza[1][1] = numero_decimal_2
    globalSeleccionCruza[1][2] = functionMath(numero_decimal_2)

    aux = []
    for v in range(0,len(auxSeleccionCruza)):
        aux += auxSeleccionCruza[v]

    globalSeleccionCruza[2][3] = aux
    print("DESCENDENCIA RESULTANTE: ")
    print(globalSeleccionCruza)

    executeMutation() #CONTINUAR DESARROLLO

def valuateSelectionIndividual(globalGeneratedIndividuals, globalPercentege):
    for i in range(0, len(globalGeneratedIndividuals)):
        if (globalGeneratedIndividuals[i] * 100) <= globalPercentegeUpdate[0]:
            print("A " + str(globalGeneratedIndividuals[i] * 100) + " " + str(globalPercentegeUpdate[i]))
            globalSeleccionCruza.append(['A', globalListX[0], globalListFX[0], globalListCromosoma[0]])

        if (globalGeneratedIndividuals[i] * 100) >= globalPercentegeUpdate[0] and (
                globalGeneratedIndividuals[
                    i] * 100) <= globalPercentegeUpdate[1]:
            print("B " + str(globalGeneratedIndividuals[i] * 100) + " " + str(globalPercentegeUpdate[i]))
            globalSeleccionCruza.append(['B', globalListX[1], globalListFX[1], globalListCromosoma[1]])


        if (globalGeneratedIndividuals[i] * 100) >= globalPercentegeUpdate[1] and (
                globalGeneratedIndividuals[
                    i] * 100) <= globalPercentegeUpdate[2]:
            print("C " + str(globalGeneratedIndividuals[i] * 100) + " " + str(globalPercentegeUpdate[i]))
            globalSeleccionCruza.append(['C', globalListX[2], globalListFX[2], globalListCromosoma[2]])



def generatedIndividuals(globalGeneratedIndividuals):
    for i in range(0, 3):
        globalGeneratedIndividuals.append(random.randrange(0, 100) / 100)
        print("GI: " + str(globalGeneratedIndividuals[i]))


def calcPercentegeAcumulated(globalPercenteges):
    percentegesAcumulatedLocal = []
    for i in range(0, len(globalPercenteges)):
        if i > 0:
            percentegesAcumulatedLocal.append(globalPercenteges[i] + percentegesAcumulatedLocal[i - 1])
            globalPercentegeUpdate.append(percentegesAcumulatedLocal[i])
        else:
            percentegesAcumulatedLocal.append(globalPercenteges[i])
            globalPercentegeUpdate.append(percentegesAcumulatedLocal[i])

    print(globalPercentegeUpdate)


def functionMath(value):
    fitness_function = (value) ** 2
    # print(fitness_function)
    return fitness_function


def processor_data(data, lista):
    lista.append(data)


def sumValueListFX(globalListFX):
    value = 0
    for j in globalListFX:
        value = value + int(j)
    return value


def executionSGA(globalListX, globalListFX):
    for i in range(0, 3):
        globalListFX.append(functionMath(globalListX[i]))
        print(globalListFX[i])

    for y in range(0, len(globalListX)):
        size = str(bin(globalListX[y])[2:]);
        listLocalCromosoma = []
        for xy in range(0, len(size)):
            listLocalCromosoma.append(size[xy])
        globalListCromosoma.append(listLocalCromosoma)

    for j in range(0, len(globalListFX)):
        globalPercentege.append(
            ((100 / sumValueListFX(globalListFX)) * globalListFX[j])
        )

    calcPercentegeAcumulated(globalPercentege)
    generatedIndividuals(globalGeneratedIndividuals)
    valuateSelectionIndividual(globalGeneratedIndividuals, globalPercentege)

    if ((random.randrange(0, 100) / 100) <= probabilityCrossing):
        print("SI CRUZA")
        executeCrossing()
    else:
        print("NO CRUZA")
        #Se debera agregar a C a la lista de resultados despues de haber mutado




if __name__ == '__main__':
    for i in range(0,3):
        #lista = [17, 28, 22]
        #iteration = i
        if firstAccess == True:
            for i in range(0, 3):
                poblacionInicial.append(random.randrange(0, 31))
                print("RAN: " + str(poblacionInicial[i]))

        globalListX = poblacionInicial
        executionSGA(globalListX, globalListFX)

