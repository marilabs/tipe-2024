import pygame
# from random import randrange
# from game import Game

# game = Game()

from game_collection import GameCollection

SIDE = 50
WIDTH = 20
HEIGHT = 15

game_collection = GameCollection(100, WIDTH, HEIGHT)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH * SIDE, HEIGHT * SIDE))
clock = pygame.time.Clock()
running = True
dt = 0

iteration = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # retrieve the new game
    game = game_collection.snake_to_display()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for (x, y) in game.snake_body:
        pygame.draw.circle(screen, "darkolivegreen3", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)

    (x, y) = game.snake_body[0]
    pygame.draw.circle(screen, "black", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 4)

    (x, y) = game.apple
    pygame.draw.circle(screen, "brown3", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)



    # update your game state here

    if not game_collection.step():
        for game in game_collection.games:
            game.snake_body = [
            (int(game.width / 2), int(game.height / 2)),
                (int(game.width / 2) + 1, int(game.height / 2)), 
                (int(game.width / 2) + 2, int(game.height / 2))
            ]
        iteration += 1
        if iteration >= 20:
            break

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(50)

pygame.quit()