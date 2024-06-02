import pygame
import os
import pickle
from game import Game
import config as c
from neural_network import NeuralNetwork

def restore_snake(brain_number: int) -> Game:
    # restore brain from file and inject it into the snake
    assert(os.path.exists(c.BRAINS_FILE))
    game = Game(c.WIDTH, c.HEIGHT, c.MAX_LIFE_POINTS, c.APPLE_LIFETIME_GAIN, c.GAME_STRATEGY, c.FITNESS_STRATEGY)
    with open(c.BRAINS_FILE, 'rb') as f:
        game_brains = pickle.load(f)
        game.brain = game_brains[brain_number]
        if c.DEBUG:
            print(game.brain, end=' ')
            print()
    return game

game = restore_snake(c.SINGLE_SNAKE_BRAIN)

# pygame setup
pygame.init()

# board contains one game/snake

CELL_SIDE = c.BOARD_SIDE // max(c.WIDTH, c.HEIGHT)
GAME_WIDTH = CELL_SIDE * c.WIDTH
GAME_HEIGHT = CELL_SIDE * c.HEIGHT

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()
running = True
dt = 0

iteration = 0

max_snake_length = 0

#? VERIFIED
while running:

    iteration += 1

    cur_fitness = game.fitness()
    cur_apple_eaten = game.apples_eaten
    if cur_apple_eaten >= max_snake_length:
        max_snake_length = cur_apple_eaten + 1

    # display game iteration and fitness of the game (generation) as window title
    info = f"Iter {iteration} - Fitness {cur_fitness:.2e} - Eaten {cur_apple_eaten} - Longest ever {max_snake_length}"

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    # draw grid
    for x in range(0, GAME_WIDTH, CELL_SIDE):
        pygame.draw.line(screen, "gray", (x, 0), (x, GAME_HEIGHT))
    for y in range(0, GAME_HEIGHT, CELL_SIDE):
        pygame.draw.line(screen, "gray", (0, y), (GAME_WIDTH, y))

    pygame.display.set_caption(info)

    for (x, y) in game.snake_body:
        pygame.draw.circle(screen, "darkolivegreen3", (x * CELL_SIDE + CELL_SIDE / 2, y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 2)
    (x, y) = game.snake_body[0] # head of the snake
    pygame.draw.circle(screen, "black", (x * CELL_SIDE + CELL_SIDE / 2, y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 4)
    (x, y) = game.apple
    pygame.draw.circle(screen, "brown3", (x * CELL_SIDE + CELL_SIDE / 2, y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 2)
    # suround the current game with a black rectangle
    pygame.draw.rect(screen, "black", (GAME_WIDTH, GAME_HEIGHT, GAME_WIDTH, GAME_HEIGHT), 1)

    # update your game state here (do not constrain snake life time)
    if not game.step(False): # snake is dead
        if iteration >= c.MAX_ITERATION:
            break
        game = restore_snake(c.SINGLE_SNAKE_BRAIN)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(25)

pygame.quit()
