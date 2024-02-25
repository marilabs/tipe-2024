import numpy as np

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))


class NeuralNetwork:

    weights = []
    biases = []
    activation_function = sigmoid
    layers_sizes = []

    """def __init__(self, layers_sizes:[int]) -> None:
        self.biases = [
            np.random.randn(i, 1) for i in layers_sizes[:1]
        ]

        self.weights = [
            np.random.randn(i, j) for (i, j) in zip(layers_sizes[1:], layers_sizes[:-1])
        ]

        self.layers_sizes = layers_sizes"""
    
    @classmethod
    def random(self, layers_sizes: [int]):
        nn = NeuralNetwork()
        nn.biases = [
            np.random.randn(i, 1) for i in layers_sizes[1:]
        ]

        nn.weights = [
            np.random.randn(i, j) for (i, j) in zip(layers_sizes[1:], layers_sizes[:-1])
        ]

        nn.layers_sizes = layers_sizes

        return nn

    def feedforward(self, activation: [float]) -> [float]:
        for (w, b) in zip(self.weights, self.biases):
            activation = sigmoid(np.dot(w, activation) + b)
        return activation
    
    def to_genome(self) -> [float]:
        genome = []
        for w in self.weights:
            for line in w:
                for c in line:
                    genome.append(c)

        for b in self.biases:
            for c in b:
                genome.append(c)

        return genome
    
    @classmethod
    def from_genome(self, genome: [float], layers: [int]):
        assert(layers != [])

        nn = NeuralNetwork()
        self.layers_sizes = layers
        
        genome = list(reversed(genome))

        nn.weights = [
            np.array([[genome.pop() for _ in range(j)] for _ in range(i)]) for (i, j) in zip(self.layers_sizes[1:], self.layers_sizes[:-1])
        ]

        nn.biases = [
            np.array([genome.pop() for _ in range(i)]) for i in self.layers_sizes[1:]
        ]
        return nn

