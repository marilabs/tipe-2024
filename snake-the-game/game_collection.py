# serpents en parallèle

from game import Game
from genetic_algorithm import GeneticAlgorithm

class GameCollection:
    games = []
    ga = GeneticAlgorithm(10)
    age = 0
    generation = 1

    def __init__(self, number_games:int, width:int, height:int) -> None:
        self.games = [Game(width, height) for _ in range(number_games)]

    def snake_to_display(self) -> Game:
        for i in range(len(self.games)):
            if not self.games[i].lost:
                return self.games[i]
        return self.games[0]
    
    def step(self) -> bool:

        self.age += 1

        one_game_not_lost = False

        for game in self.games:
            if not game.lost:
                one_game_not_lost = True
                game.step()

        # if all games are lost, evolve
        if not one_game_not_lost:
            self.evolve()

        """# if the displayed game is lost, evolve to avoid waiting with a frozen snake
        if self.games[0].lost:
            self.evolve() """

        return one_game_not_lost
    

    def evolve(self):

        new_population = self.ga.evolve([
            (game.brain, game.fitness(self.age))
            for game in self.games
        ])

        width, height = self.games[0].width, self.games[0].height

        for i in range(len(new_population)):

            g = Game(width, height)
            g.brain = new_population[i]
            self.games[i] = g

        self.age = 0
        self.generation += 1

        
    