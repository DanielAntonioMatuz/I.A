import math
import random
from tkinter import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
# ALGORITMO DE ENTRENAMIENTO PARA EL PROBLEMA AND

# PARAMETROS DEL SISTEMA
W = np.empty([3])
Yc = np.empty([4])
E = np.zeros(4)
ET = np.zeros(4)
ETX = np.zeros(4)
NETX = np.zeros(4)
E1 = np.empty(4)
arrayErr = []
arryGen = []
sigmuidal = []
k = 0
n = 0.5
CS = 0.01  #CONDICIÓN DE SALIDA
e = 0
ANDOR = False



def GRAPHIC_PLOT():
    x = arrayErr
    y = arryGen
    plt.title("Evolución ECM")
    plt.plot(y, x, color="green", label="VALORES DEL ECM POR ITERACIÓN")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # PASO 1 - GENERAR LOS PESOS ALEATORIOS
    for i in range(3):
        W[i] = (random.randrange(100) / 100)
        print(W[i])

    # W[0] = 0.98
    # W[1] = 0.81
    # W[2] = 1.00

    # PASO 2 - DEFINIR VALORES DE ENTRADA
        X = [[1, 0, 0],
             [1, 0, 1],
             [1, 1, 0],
             [1, 1, 1]]

    if ANDOR:
        #AND
        Y = [[0], [0], [0], [1]]
    else:
        #OR
        Y = [[0], [1], [1], [1]]

    while True:
        k = k + 1
        arryGen.append(k)
        # PASO 3 - CALCULAR LA SALIDA DE LA NEURONA

        # U = X x W^T
        W = np.transpose(W)
        U = np.matmul(X, W)

        # Yc = FA(U)
        for i in range(len(U)):
            if U[i] > 0:
                Yc[i] = 1
                print(Yc[i])
            else:
                Yc[i] = 0
                print(Yc[i])

        # E = Y - Yc
        for i in range(len(Y)):
            E[i] = Y[i] - Yc[i]

        # OBTENER LA TRANSPUESTA DE E
        ET = np.transpose(E)

        # ELEVAR AL CUADRADO CADA POSICION DE E
        for i in range(len(ET)):
            E1[i] = (ET[i] ** 2)

        # PASO 4 -  W(K + 1) = W(K) + n [E(K)^T X] | ACTUALIZAR LOS PESOS
        ETX = np.matmul(ET, X)
        for i in range(len(ETX)):
            NETX[i] = ETX[i] * n

        for j in range(len(W)):
            W[j] = W[j] + NETX[j]

        # VALORES ABSOLUTOS DE ERROR CUADRÁTICO MEDIO
        e = "{0:.2f}".format(math.sqrt(sum(abs(E1))))
        arrayErr.append(float(e))

        print("ITERACIÓN: ", k)
        print("RESULTADO DE ENTRENAMIENTO: ", Yc, " SALIDA ESPERADA: ", Y)
        print("ECM", e)

        if float(e) <= CS:
            break

    print(arrayErr)
    print("E: ", E)
    print("RESULTADO DE ENTRENAMIENTO: ", Yc)
    GRAPHIC_PLOT()
