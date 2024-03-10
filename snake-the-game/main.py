import pygame
import os
import signal
import sys

from game_collection import GameCollection

SIDE = 50
WIDTH = 20
HEIGHT = 15
NUMBER_GAMES = 500

game_collection = GameCollection(NUMBER_GAMES, WIDTH, HEIGHT)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH * SIDE, HEIGHT * SIDE))
clock = pygame.time.Clock()
running = True
dt = 0

def save_and_exit(signal, frame):
    game_collection.save_to_file('saved_game_collection.pickle')
    sys.exit(0)

# save program state in case of interuption
signal.signal(signal.SIGINT, save_and_exit)

iteration = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # retrieve the new game
    game, current_snake = game_collection.snake_to_display()

    # display game iteration and fitness of the game (generation) as window title
    pygame.display.set_caption(f"Generation {game_collection.generation} - Current snake {current_snake} - Iteration {game_collection.iteration} - Fitness {game.fitness()}")

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
        if iteration >= 50:
            break

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(50)

game_collection.save_to_file('saved_game_collection.pickle')

pygame.quit()