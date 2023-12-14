import numpy as np

from neural_network import NeuralNetwork

class GeneticAlgorithm:

    save_bests = 0
    k = 5 # avant: 1
    mut_chance = 0.3 # avant: 0.1
    coeff = 0.3 # avant: 0.1

    def __init__(self, save_bests: int) -> None:
        self.save_bests = save_bests

    def select_parent(self, population: [NeuralNetwork, int]) -> NeuralNetwork: 
        # Roulette-wheel selection: numpy.random.choice
        maxi = sum([x[1] for x in population])
        selection_probability = [x[1] / maxi for x in population]
        parent1, parent2 = np.random.choice(len(population), p=selection_probability), np.random.choice(len(population), p=selection_probability)
        return population[parent1][0], population[parent2][0]

    def crossover(self, parent_a: [float], parent_b: [float]) -> [float]:
        """
        K-point crossover cf Wikipedia:
        - select k random points in range(len(parent_a))
        - create a new array which alternate between coefficients of parent_a and parent_b
        """
        n = len(parent_a)
        l = sorted([np.random.randint(0, n) for _ in range(self.k)])
        l.append(-1)
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

    def mutate(self, genome: [float]) -> None:
        """
        Gaussian mutation:
        - for each coefficient:
            - if random() <=  mutation chance (paramètre réglé):
                - generate a sign at random
                - generate an amplitude (between 0 and 1)
                - add sign * amplitude * coeff to the coefficient (coeff is a parameter)
        """
        for g in genome:
            if np.random.random() <= self.mut_chance:
                sign = 1 if np.random.random() <= 0.5 else -1
                amplitude = np.random.random()
                g += sign * amplitude * self.coeff

    def evolve(self, population: [NeuralNetwork, int]) -> list:
        assert(len(population) != 0)

        new_population = []

        # sélection des meilleurs
        population.sort(key=lambda x : x[1], reverse=True)

        for i in range(len(population)):
            if i < self.save_bests:
                new_population.append(population[i][0])
            else:
                parent_a, parent_b = self.select_parent(population)

                parent_a, parent_b = parent_a.to_genome(), parent_b.to_genome()

                child = self.crossover(parent_a, parent_b)

                self.mutate(child)

                new_population.append(NeuralNetwork.from_genome(child, population[i][0].layers_sizes))

        return new_population
    
