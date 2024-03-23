import numpy as np

from neural_network import NeuralNetwork
from typing import List, Tuple
import copy

class GeneticAlgorithm:
    
    def __init__(self, save_bests: int = 10, k: int = 5, mut_chance: float = 0.5, coeff: float = 0.5) -> None:
        self.save_bests = save_bests
        self.k = k
        self.mut_chance = mut_chance
        self.coeff = coeff

    def select_parent(self, population: List[Tuple[NeuralNetwork, int]]) -> Tuple[NeuralNetwork, NeuralNetwork]:
        # Roulette-wheel selection: numpy.random.choice
        maxi = sum([x[1] for x in population])
        selection_probability = [x[1] / maxi for x in population]
        parent1, parent2 = np.random.choice(len(population), p=selection_probability), np.random.choice(len(population), p=selection_probability)
        return population[parent1][0], population[parent2][0]

    def crossover(self, parent_a: List[float], parent_b: List[float]) -> List[float]:
        """
        K-point crossover cf Wikipedia:
        - select k random points in range(len(parent_a))
        - create a new array which alternate between coefficients of parent_a and parent_b
        """
        n = len(parent_a)
        # list of crossover points
        l = sorted([np.random.randint(0, n) for _ in range(self.k)]) # to avoid having two times the same index
        l.append(-1) # to avoid index out of range but never ued
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

    def mutate(self, genome: List[float]) -> None:
        """
        Gaussian mutation:
        - for each coefficient:
            - if random() <=  mutation chance (paramètre réglé):
                - generate a sign at random
                - generate an amplitude (between 0 and 1)
                - add sign * amplitude * coeff to the coefficient (coeff is a parameter)
        """
        for i in range(len(genome)):
            if np.random.random() <= self.mut_chance:
                sign = 1 if np.random.random() <= 0.5 else -1
                amplitude = np.random.random()
                genome[i] += sign * amplitude * self.coeff

    #? VERIFIED genetic_algorithm/src/libs.rs
    def evolve(self, population: Tuple[NeuralNetwork, int]) -> list:
        assert(len(population) != 0)
        new_population = []
        # sélection des meilleurs
        population.sort(key=lambda x : x[1], reverse=True)
        for i in range(len(population)):
            if i < self.save_bests:
                new_population.append(copy.deepcopy(population[i][0])) # to avoid reference
            else:
                parent_a, parent_b = self.select_parent(population)
                child = self.crossover(parent_a.to_genome(), parent_b.to_genome())
                self.mutate(child)
                new_population.append(NeuralNetwork.from_genome(child, population[i][0].layers_sizes))
        return new_population
    
