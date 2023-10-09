# serpents en parallèle

from game import Game

class GameCollection:
    games = []

    def __init__(self, number_games:int, width:int, height:int) -> None:
        self.games = [Game(width, height) for _ in range(number_games)]

    def snake_to_display(self) -> Game:
        return self.games[0]
    
    def step(self) -> bool:
        one_game_not_lost = False
        for game in self.games:
            if not game.lost:
                one_game_not_lost = True
                game.step()

        return one_game_not_lost
    