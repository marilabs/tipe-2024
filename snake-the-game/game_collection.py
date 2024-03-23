# serpents en parallèle

from game import Game
from genetic_algorithm import GeneticAlgorithm
import pickle
import config as c
import math
from typing import List, Tuple

class GameCollection:
    games = []
    ga = GeneticAlgorithm(math.ceil(c.PORTION_BESTS * c.POPULATION / 100), c.NUMBER_CROSSOVER_POINTS, c.MUTATION_CHANCE, c.MUTATION_COEFF)
    iteration = 0
    generation = 1

    def __init__(self, number_games:int, width:int, height:int) -> None:
        self.games = [Game(width, height, c.MAX_LIFE_POINTS, c.APPLE_LIFETIME_GAIN) for _ in range(number_games)]

    def snake_to_display(self) -> Tuple[Game, int]:
        for i in range(len(self.games)):
            if not self.games[i].lost:
                return self.games[i], i
        return self.games[0], 0

    def longest_snake(self) -> Tuple[Game, int]:
        longest = 0
        index = 0
        for i in range(len(self.games)):
            if len(self.games[i].snake_body) > longest:
                longest = len(self.games[i].snake_body)
                index = i
        return self.games[index], index

    def step(self) -> bool:

        self.iteration += 1

        one_game_not_lost = False

        for game in self.games:
            if not game.lost:
                one_game_not_lost = True
                game.step()

        # if all games are lost, evolve
        if not one_game_not_lost:
            self.evolve()
        return one_game_not_lost


    def evolve(self):

        new_population = self.ga.evolve([
            (game.brain, game.fitness())
            for game in self.games
        ])

        width, height = self.games[0].width, self.games[0].height

        for i in range(len(new_population)):
            g = Game(width, height, c.MAX_LIFE_POINTS, c.APPLE_LIFETIME_GAIN) # create new game
            g.brain = new_population[i] # inject brain in game
            self.games[i] = g # replace current game with new one

        self.iteration = 0
        self.generation += 1

    def save_brains(self, filename):
        # save the game collection and all the games in the game collection to a file
        #for game in self.games:
        #    print(game.brain.layers_sizes)
        game_brains = [game.brain for game in self.games]
        if c.DEBUG:
            for brain in game_brains:
                print(brain.weights, end=' ')
            print()
        print("save_brains: len(game_brains): ", len(game_brains))
        with open(filename, 'wb') as f:
            pickle.dump(game_brains, f)

    def restore_brains(self, filename):
        with open(filename, 'rb') as f:
            game_brains = pickle.load(f)
            print("restore_brains: len(game_brains): ", len(game_brains))
            for i in range(len(self.games)):
                self.games[i].brain = game_brains[i]
            if c.DEBUG:
                for brain in game_brains:
                    print(brain.weights, end=' ')
                print()

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def best_fitness(self):
        return max(game.fitness() for game in self.games)

    def average_fitness(self):
        return sum(game.fitness() for game in self.games) / len(self.games)

    def max_apple_eaten(self):
        return max(game.apples_eaten for game in self.games)
