# serpents en parallèle

from game import Game
from genetic_algorithm import GeneticAlgorithm
import pickle

class GameCollection:
    games = []
    # GeneticAlgorithm(10) : 10 bests are saved
    ga = GeneticAlgorithm(10)
    iteration = 0
    generation = 1

    def __init__(self, number_games:int, width:int, height:int) -> None:
        self.games = [Game(width, height) for _ in range(number_games)]

    def snake_to_display(self) -> (Game, int):
        for i in range(len(self.games)):
            if not self.games[i].lost:
                return self.games[i], i
        return self.games[0], 0

    def longest_snake(self) -> (Game, int):
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
            g = Game(width, height) # create new game
            g.brain = new_population[i] # inject brain in game
            self.games[i] = g # replace current game with new one

        self.iteration = 0
        self.generation += 1

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

        
    