import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

arraySigmoid = []

class Perceptron:

    def __init__(self, inputs, outputs):
        self.inputs = np.array(inputs)
        self.outputs = np.array(outputs)

    def Fit(self):

        epochs, num_inputs = 0, 0

        while num_inputs < 4:
            print('---------- Iteraciones {} ---------- '.format(epochs))

            # se generan pesos aleatorios en el rango [-1,1]
            weights = np.array(np.random.uniform(-1, 1, self.inputs.shape))
            for input, weight, output in zip(self.inputs, weights, self.outputs):

                # Realiza la suma ponderada de entradas con pesos
                y_generate = input @ weight

                # Función sigmoide
                y_generate = 0 if y_generate < 0 else 1
                arraySigmoid.append(y_generate)

                if y_generate == output:
                    num_inputs += 1
                else:
                    num_inputs = 0

                print('entrada: ', input, 'pesos:', weight, 'salida_esperada: ', output, 'salida_obtenida: ',
                      y_generate)

            epochs += 1

        return True



def GRAPHIC_PLOT():
    x = arraySigmoid
    plt.title("Evolución ECM")
    plt.plot(x, color="green", label="VALORES DEL ECM POR ITERACIÓN")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    inputs = [
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1]
    ]

    outputs = [0, 0, 0, 1]

    perceptron = Perceptron(inputs, outputs)
    perceptron.Fit()
    GRAPHIC_PLOT()
