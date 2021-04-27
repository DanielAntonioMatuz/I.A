from ypstruct import structure
import numpy as np

def run(problem, params):
    costfunc =  problem.costfunc
    nvar = problem.nvar
    varmin = problem.varmin
    varmax = problem.varmax

    #Parametros
    maxit = params.maxit
    npop = params.npop
    pc = params.pc
    nc = int(np.round(pc*npop/2))
    gamma = params.gamma
    mu = params.mu
    sigma = params.sigma

    # Plantilla de individuo vacio
    empty_individual = structure()
    empty_individual.position = None
    empty_individual.cost = None

    # Mejor solucion
    bestsol = empty_individual.deepcopy()
    bestsol.cost = np.inf

    # Inicializar la poblacion
    pop = empty_individual.repeat(npop)
    for i in range(0, npop):
        pop[i].position = np.random.uniform(varmin, varmax, nvar)
        pop[i].cost = costfunc(pop[i].position)
        if pop[i].cost < bestsol.cost:
            bestsol = pop[i].deepcopy()

    # Mejor Fitness de las iteraciones
    bestcost = np.empty(maxit)

    # Bucle principal
    for it in range(maxit):
        popc = []
        for k in range(nc//2):
            # Seleccion de los padres aleatoriamente
            q = np.random.permutation(npop)
            p1 = pop[q[0]] # Padre 1
            p2 = pop[q[1]] # Padre 2

            # Proceso de cruzamiento
            c1, c2 = crossover(p1, p2, gamma)

            # Proceso de mutacion
            c1 = mutate(c1, mu, sigma)
            c2 = mutate(c2, mu, sigma)

            #Apply bounds
            apply_bound(c1, varmin, varmax)
            apply_bound(c2, varmin, varmax)

            # Evaluar descendencia
            c1.cost = costfunc(c1.position)
            if c1.cost < bestsol.cost:
                bestsol = c1.deepcopy()

            c2.cost = costfunc(c2.position)
            if c2.cost < bestsol.cost:
                bestsol = c2.deepcopy()

            # Agregarlo a la solucion
            popc.append(c1)
            popc.append(c2)

        # Verificar, ordenar y seleccionar mejores individuos para siguiente generacion
        pop += popc
        pop = sorted(pop, key=lambda x: x.cost)
        pop = pop[0:npop]


        bestcost[it] = bestsol.cost
        print("Iteration {}: Best Cost = {}".format(it,bestcost))




    # Salida
    out = structure()
    out.pop = pop
    out.bestsol = bestsol
    out.bestcost = bestcost
    return out

def crossover(p1, p2, gamma=0.1):
    c1 = p1.deepcopy()
    c2 = p2.deepcopy()
    alpha = np.random.uniform(-gamma, 1+gamma, *c1.position.shape)
    c1.position = alpha * p1.position + (1 - alpha) * p2.position
    c2.position = alpha * p2.position + (1 - alpha) * p1.position

def mutate(x, mu, sigma):
    y = x.deepcopy()
    flag = np.random.rand(*x.position.shape) <= mu
    ind = np.argwhere(flag)
    y.position[ind] += sigma * np.random.rand(*ind.shape)
    return y

def apply_bound(x,varmin,varmax):
    x.position = np.maximum(x.position, varmin)
    x.position = np.minimum(x.position, varmax)