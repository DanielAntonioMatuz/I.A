import random
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template
import time
from tkinter import *
import tk as tk
import webbrowser


############################################################################################
# Configuracion de datos predefinidos en la lista de datos del sistema
############################################################################################
dataEvaluationFitness = []
passData = []
passData.append("EnAPAciateNtANTikATIgHTENtIGNerbARePtintAGEOnTreaT")
passData.append("500")
passData.append("key_data")
passData.append("0 Generaciones | 0.0 minutos")
passData.append("Sin datos")
passData.append("0")
passData.append("passowrd_key_generator")
passData.append("score_security_password")
primary_key_base = "NerbARePtintAGEOnTreaT"
secondary_key_base = "teNtANTikATIgHTE"


############################################################################################
# Configuración del UI del SGA
############################################################################################

window = Tk()

window.title("Configuraciones del SGA | Desencriptador de contraseñas")
window.geometry('700x150')

lbl = Label(window, text="Ingrese su contraseña : ")
lbl.grid(column=0, row=0)

txt = Entry(window, width=80)
txt.grid(column=1, row=0)


lbl = Label(window, text="Ingrese tamaño poblacion: ")
lbl.grid(column=0, row=1)

txt2 = Entry(window, width=80)
txt2.grid(column=1, row=1)

lbl = Label(window, text="Ingrese datos iniciales: ")
lbl.grid(column=0, row=2)

txt3 = Entry(window, width=80)
txt3.grid(column=1, row=2)



def clicked():
    if len(txt.get()) >= 2:
        passData[0] = str(txt.get())
    else:
        passData[0] = "EnAPAciateNtANTikATIgHTENtIGNerbARePtintAGEOnTreaT"

    if txt2.get() != "":
        if int(txt2.get()) >= 2:
            passData[1] = str(txt2.get())
        else:
            passData[1] = "500"
    else:
        passData[1] = "500"

    if len(txt3.get()) == len(txt.get()):
        passData[2] = str(txt3.get())
    else:
        passData[2] = ""

    print("POP LENGHT: ", passData[1])
    print("COMPARTE E to E: ", passData[2])


btn = Button(window, text="Configurar datos", command=clicked)
btn.grid(column=2, row=0)
window.mainloop()



lista_alfabeto = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', ' ', '¡']

# crear contraseña
password_key = passData[0]
secret_password = list(password_key)
# tamnaño de la contraseña
password_length = len(secret_password)
# El tamaño de la población
poblacion_tamanio = int(passData[1])
# Numero de padres generados
num_padres = 20
# Numero de población que se mantendrá en cada iteración
poblation_sig = 2
password_accept = True

app = Flask(__name__)
value = []
i = 0



@app.route('/')
def homepage():
    return render_template("index.html", exitData=value, systemData=passData, generations=generaciones, fitness=fitness_datos)



############################################################################################
# Generar población inicial de busqueda para desencriptar
############################################################################################
population = []
def poblacionInicial():

   if passData[2] == "":
       for i in range(poblacion_tamanio):

           chromosome = []
           for x in range(password_length):
               chromosome.append(random.choice(lista_alfabeto))

           population.append(chromosome)
   else:
       dataAux = passData[2]
       print("ALSMASKJA")
       for i in range(poblacion_tamanio):

           chromosome = []
           for x in range(password_length):
               chromosome.append(dataAux[x])

           population.append(chromosome)



# Calculo de fitness
def fitness(population):
    fitness_scores = []
    for chromosome in population:
        matches = 0
        for index in range(password_length):
            if secret_password[index] == chromosome[index]:
                matches += 1
        result = [chromosome,matches]
        fitness_scores.append(result)
    return fitness_scores




# seleccion de padres
def seleccionar_padres(fitness_scores):
    parents_list = []
    for chromosome in sorted(fitness_scores, key=lambda x: x[1], reverse=True)[:num_padres]:
        parents_list.append(chromosome[0])
    return(parents_list)




# Seleccion de padres por torneo para cruza
def proceso_organizacion_torn(p1, p2):
    Hijos_List = []

    p1 = padres[0]
    p2 = padres[1]

    geneA = int(random.random() * password_length)
    geneB = int(random.random() * password_length)

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(0, password_length):
        if (i < startGene) or (i > endGene):
            Hijos_List.append(p1[i])
        else:
            Hijos_List.append(p2[i])
    return Hijos_List




# Proceso de cruza y actualizacion
def proceso_cruza_organizacion(parents_pool):
    hijos_list = []
    num_new_children = len(population) - poblation_sig

    for i in range(0, poblation_sig):
        hijos_list.append(parents_pool[i])

    for i in range(0,num_new_children):
        P1 = parents_pool[int(random.random() * len(parents_pool))]
        P2 = parents_pool[int(random.random() * len(parents_pool))]
        hijos_list.append(proceso_organizacion_torn(P1, P2))
    return hijos_list



# Proceso de mutacion
def proceso_mutacion(hijos_datos):
    for i in range(len(hijos_datos)):
        if random.random() > 0.1:
            continue
        else:
            posicion_mutacion = int(random.random() * password_length)
            mutacion_p = random.choice(lista_alfabeto)
            hijos_datos[i][posicion_mutacion] = mutacion_p
    return hijos_datos

def functionFitnessSecurityScore(fitness_datos):
    dataEvaluationFitness = []
    a = password_length
    x = 0
    try:
        if int(password_key):
            for i in range(0, len(fitness_datos)):
                dataEvaluationFitness.append(0)
    except:
        for i in range(0, len(fitness_datos)):
            x = fitness_datos[i]
            dataEvaluationFitness.append(round(
                (np.sin(x) + (x ** 2) + (x + 1))) / a * 2) #Funcion de calculo de seguridad

    return dataEvaluationFitness

def graficarDatos():
    fig = plt.figure()
    plt.plot(list(range(generaciones + 1)), fitness_datos, label="Mejor Fitness")
    plt.plot(dataEvaluationFitness, color="green", label="Nivel de seguridad")
    fig.suptitle('Puntaje de Fitness por generación de busqueda', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Generación')
    ax.set_ylabel('Puntaje de Fitness')
    plt.legend()
    plt.savefig('static/export_graphic.png')
    plt.show()

def generatorNewPassword():
    poblacionInicial()
    varAuxPass = value[password_length-1] + secondary_key_base + password_key + primary_key_base
    return varAuxPass


############################################################################################
# Ejecutar GA
############################################################################################

if __name__ == '__main__':
    poblacionInicial()
    fitness_datos = []
    soluciones = []
    generaciones = 0
    tiempo_ejecucion = time.time()
    password_accept = True

    while True:
        fitness_scores = fitness(population)
        fitness_datos.append(max([i[1] for i in fitness_scores]))
        soluciones.append(''.join([i[0] for i in fitness_scores if i[1] == max([i[1] for i in fitness_scores])][0]))
        varAux = ''.join([i[0] for i in fitness_scores if i[1] == max([i[1] for i in fitness_scores])][0])
        value.append(varAux)
        print(varAux)
        value[0] = varAux
        if max([i[1] for i in fitness_scores]) == password_length:
            print("Descifrado en {} genraciones, y un tiempo de: {} seconds! \nContraseña desbloqueda: = {} \nContraseña ingresada por el usuario: = {}".format(
                generaciones, time.time() - tiempo_ejecucion, ''.join(secret_password),
                ''.join([i[0] for i in fitness_scores if i[1] == password_length][0])))
            break
        padres = seleccionar_padres(fitness_scores)
        hijos = proceso_cruza_organizacion(padres)
        population = proceso_mutacion(hijos)
        generaciones += 1
        passData[3] = "Generaciones: " + str(generaciones) + " | Tiempo: " + str(time.time() - tiempo_ejecucion)

        if len(value) > 2:
            passData[2] = value[1]

    passData[7] = functionFitnessSecurityScore(fitness_datos)
    passData[7] = passData[7][generaciones]
    dataEvaluationFitness = functionFitnessSecurityScore(fitness_datos)


    if (time.time() - tiempo_ejecucion) > 9 and generaciones >= 95 and float(passData[7]) > 52.0:
        passData[5] = "85"
        passData[4] = "Compleja - segura"
        if password_length > 40:
            passData[5] = "100"
        if password_length > 35 and password_length <= 40:
            passData[5] = "75"
        passData[6] = "Tu contraseña es completamente segura y cumple con las condiciones"

    if float(passData[7]) < 52:
        passData[4] = "Es segura, pero no cumple las condiciones"
        passData[5] = "45"
        passData[6] = generatorNewPassword()

    if (time.time() - tiempo_ejecucion) <= 9 and (time.time() - tiempo_ejecucion) >= 4.1 and generaciones >= 95:
        passData[4] = "Aceptable"
        passData[5] = "70"
        if password_length > 25 and password_length <= 35:
            passData[5] = "69"
        if password_length > 20 and password_length <= 15:
            passData[5] = "60"

        passData[6] = password_key + ''.join([i[0] for i in fitness_scores if i[1] == max([i[1] for i in fitness_scores])][0]) + ''.join([i[0] for i in fitness_scores if i[1] == max([i[1] for i in fitness_scores])][0])

        if float(passData[7]) >= 52.0:
            passData[6] = "Tu contraseña cumple con las condiciones mínimas y es segura"
        else:
            passData[6] = generatorNewPassword()
            passData[4] = "Es segura, pero no cumple las condiciones"
            passData[5] = "41"


    if (time.time() - tiempo_ejecucion) <= 4:
        passData[4] = "Critico - nada/poco seguro"
        passData[5] = "10"
        if password_length > 15 and password_length <= 11:
            passData[5] = "29"
        if password_length <= 11:
            passData[5] = "5"
        passData[6] = generatorNewPassword()
    try:
        if int(password_key):
            passData[4] = "Critico - nada/poco seguro"
            passData[5] = "10"
            passData[6] = generatorNewPassword()
            passData[7] = 0.0
    except:
        print("")


    print("Score del nivel de la seguridad de la contraseña: ", passData[7])

    graficarDatos()
    webbrowser.open("http://127.0.0.1:5000/", new=2, autoraise=True)
    app.run()


