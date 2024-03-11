import pygame
import os
import signal
import sys

from game_collection import GameCollection

SIDE = 30
WIDTH = 10
HEIGHT = 10
NUMBER_GAMES = 500 # number of games in the collection -> number of snakes in parallel
MAX_ITERATION = 50 # number of iterations before stopping the program

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
    #game, current_snake = game_collection.longest_snake() # to see the longest snake


    # display game iteration and fitness of the game (generation) as window title
    pygame.display.set_caption(f"Gen {game_collection.generation} - Cur snake {current_snake} - Iter {game_collection.iteration} - Fitness {game.fitness()} - Max fitness {game_collection.best_fitness()} - Avg fitness {game_collection.average_fitness()} - Max eaten {game_collection.max_apple_eaten()}")
    # print the same on console
    print(f"Gen {game_collection.generation} - Cur snake {current_snake} - Iter {game_collection.iteration} - Fitness {game.fitness()} - Max fitness {game_collection.best_fitness()} - Avg fitness {game_collection.average_fitness()} - Max eaten {game_collection.max_apple_eaten()}")

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for (x, y) in game.snake_body:
        pygame.draw.circle(screen, "darkolivegreen3", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)

    (x, y) = game.snake_body[0]
    pygame.draw.circle(screen, "black", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 4)

    (x, y) = game.apple
    pygame.draw.circle(screen, "brown3", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)

    # update your game state here

    if not game_collection.step(): # all sakes in collection dead go next iteration
        iteration += 1
        if iteration >= MAX_ITERATION:
            break

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(50)

game_collection.save_to_file('saved_game_collection.pickle')

pygame.quit()