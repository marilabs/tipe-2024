import numpy as np

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))


class NeuralNetwork:

    weights = []
    biases = []
    activation_function = sigmoid

    def __init__(self, layers_sizes:[int]) -> None:
        self.biases = [
            np.random.randn(i, 1) for i in layers_sizes[:1]
        ]

        self.weights = [
            np.random.randn(i, j) for (i, j) in zip(layers_sizes[1:], layers_sizes[:-1])
        ]

    def feedforward(self, activation: [float]) -> [float]:
        for (w, b) in zip(self.weights, self.biases):
            activation = sigmoid(np.dot(w, activation) + b)
        return activation
    

