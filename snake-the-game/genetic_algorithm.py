import numpy as np

from neural_network import NeuralNetwork

class GeneticAlgorithm:

    save_bests = 0

    def __init__(self, save_bests: int) -> None:
        self.save_bests = save_bests

    def select_parent(self, population: [NeuralNetwork, int]) -> NeuralNetwork: 
        # Roulette-wheel selection: numpy.random.choice
        maxi = sum([x[1] for x in population])
        selection_probability = [x[1] / maxi for x in population]
        parent = np.random.choice(len(population), p=selection_probability)
        return population[parent][0]

    def crossover(parent_a: [float], parent_b: [float]) -> [float]:
        """
        K-point crossover cf Wikipedia:
        - select k random points in range(len(parent_a))
        - create a new array which alternate between coefficients of parent_a and parent_b
        """
        n = len(parent_a)
        k = 5
        l = sorted([np.random.randint(0, n) for i in range(k)])
        child = []
        current_parent = 0
        current_index = 0
        for i in range(n):
            if i == l[current_index]:
                current_parent = 1 - current_parent
                current_index += 1
            if current_parent == 0:
                child.append(parent_a[i])
            else:
                child.append(parent_b[i])
        return child

    def mutate(genome: [float]) -> None:
        """
        Gaussian mutation:
        - for each coefficient:
            - if random() <=  mutation chance (paramètre réglé):
                - generate a sign at random
                - generate an amplitude (between 0 and 1)
                - add sign * amplitude * coeff to the coefficient (coeff is a parameter)
        """
        pass

    def evolve(self, population: [NeuralNetwork, int]) -> list:
        assert(len(population) != 0)

        new_population = []

        # sélection des meilleurs
        population = population.sort(lambda x : x[0], reverse=True)

        for i in range(len(population)):
            if i < self.save_bests:
                new_population.append(population[i][0])
            else:
                parent_a = self.select_parent(population).to_genome()
                parent_b = self.select_parent(population).to_genome()

                child = self.crossover(parent_a, parent_b)

                self.mutate(child)

                new_population.append(NeuralNetwork.from_genome(child, population[i].layers_sizes))

