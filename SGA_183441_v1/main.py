import numpy as np
import matplotlib.pyplot as plt
from ypstruct import structure
import ga

# Funcion del SGA
def spehere(x):
    return sum(x**2)

# Definicion del problema
problem = structure()
problem.constfunc = spehere
problem.nvar = 5
problem.varmin = -10
problem.varmax = 10

# Parametros del SGA
params = structure
params.maxit = 100
params.npop = 20
params.pc = 1
params.gamma = 0.1
params.mu = 0.1
params.sigma = 0.1

# Ejecucion de SGA
out = ga.run(problem, params)

# Resultados