import numpy as np
from typing import List

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

class NeuralNetwork:

    layers_sizes = []
    weights = []
    biases = []
    activation_function = None

    def __init__(self, layers_sizes:List[int]) -> None:
        self.biases = [np.random.randn(i, 1) for i in layers_sizes[1:]]
        self.weights = [np.random.randn(i, j) for (i, j) in zip(layers_sizes[1:], layers_sizes[:-1])]
        self.activation_function = sigmoid
        self.layers_sizes = layers_sizes

    def feedforward(self, activation):
        for w, b in zip(self.weights, self.biases):
            activation = self.activation_function(np.dot(w, activation) + b)
        return activation

    """
    def to_genome(self) -> List[float]:
        genome = []
        for w in self.weights:
            for line in w:
                for c in line:
                    genome.append(c)
        for b in self.biases:
            for c in b:
                genome.append(c)
        return genome
    """

    def to_genome(self) -> List[float]:
        genome = np.concatenate([w.flatten() for w in self.weights] + [b.flatten() for b in self.biases])
        return genome.tolist()

    @classmethod
    def from_genome(cls, genome: List[float], layers: List[int]):
        assert len(layers) > 0
        nn = cls(layers)
        # this code is more efficient than the commented code below because it avoids the list inversions
        offset = 0
        for i, (j, k) in enumerate(zip(layers[:-1], layers[1:])):
            nn.weights[i] = np.reshape(genome[offset:offset + j * k], (k, j))
            offset += j * k
        for i, k in enumerate(layers[1:]):
            nn.biases[i] = np.reshape(genome[offset:offset + k], (k, 1))
            offset += k
        """
        genome = list(reversed(genome))
        nn.weights = [np.array([[genome.pop() for _ in range(j)] for _ in range(i)]) for (i, j) in zip(nn.layers_sizes[1:], nn.layers_sizes[:-1])]
        nn.biases = [np.array([genome.pop() for _ in range(i)]) for i in nn.layers_sizes[1:]]
        """
        return nn
