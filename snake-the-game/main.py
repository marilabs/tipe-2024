import pygame
import os
import signal
import sys
from game_collection import GameCollection
import math
import matplotlib.pyplot as plt
import numpy as np
import config as c
from scipy.interpolate import make_interp_spline
import pickle
import sys

game_collection = GameCollection(c.POPULATION, c.WIDTH, c.HEIGHT)

if c.RESTORE and os.path.exists(c.BRAINS_FILE):
    game_collection.restore_brains(c.BRAINS_FILE)
# board with all populations has games_per_side games per side
# each game has WIDTH x HEIGHT cells

if c.DISPLAY_ALL_POPULATION:
    games_per_side = math.ceil(math.sqrt(c.POPULATION))
else:
    games_per_side = 1

CELL_SIDE = (c.BOARD_SIDE // games_per_side) // max(c.WIDTH, c.HEIGHT)
GAME_WIDTH = CELL_SIDE * c.WIDTH
GAME_HEIGHT = CELL_SIDE * c.HEIGHT
BOARD_WIDTH = games_per_side * GAME_WIDTH
BOARD_HEIGHT = games_per_side * GAME_HEIGHT

print(f"CELL_SIDE: {CELL_SIDE}, GAME_WIDTH: {GAME_WIDTH}, GAME_HEIGHT: {GAME_HEIGHT}, BOARD_WIDTH: {BOARD_WIDTH}, BOARD_HEIGHT: {BOARD_HEIGHT}")

if c.DISPLAY_GRAPHICS:
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = pygame.time.Clock()

running = True
dt = 0

iteration = 0

max_fitness = []
min_fitness = []
avg_fitness = []
max_apple_eaten = []
min_apple_eaten = []
avg_apple_eaten = []
max_snake_length = 0

def save_curves(filename):
    with open(filename, 'wb') as f:
        pickle.dump((max_fitness, min_fitness, avg_fitness, max_apple_eaten, min_apple_eaten, avg_apple_eaten, max_snake_length), f)

def restore_curves(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def save_and_exit(signal, frame):
    if c.SAVE:
        game_collection.save_brains(c.BRAINS_FILE)
        save_curves(c.CURVES_FILES)
    sys.exit(0)

# save program state in case of interruption
signal.signal(signal.SIGINT, save_and_exit)

while running:

    cur_max_fitness = game_collection.best_fitness()
    cur_min_fitness = game_collection.worst_fitness()
    cur_avg_fitness = game_collection.average_fitness()
    cur_max_apple_eaten = game_collection.max_apple_eaten()
    cur_min_apple_eaten = game_collection.min_apple_eaten()
    cur_avg_apple_eaten = game_collection.average_apple_eaten()

    if cur_max_apple_eaten >= max_snake_length:
        max_snake_length = cur_max_apple_eaten + 1

    # retrieve the new game
    if c.DISPLAY_LARGEST_SNAKE:
        game, current_snake = game_collection.longest_snake() # to see the longest snake
    else:
        game, current_snake = game_collection.snake_to_display()

    # display game iteration and fitness of the game (generation) as window title
    #info = f"Gen {game_collection.generation} - Iter {game_collection.iteration} - Fitness {game.fitness():.2e} - Max fitness {cur_max_fitness:.2e} - Avg fitness {round(cur_avg_fitness, 2):.2e} - Max eaten {cur_max_apple_eaten} - Longest ever {max_snake_length}"
    info = f"Gen {game_collection.generation} - Iter {game_collection.iteration} - Fitness ({cur_min_fitness:.1e}:{cur_avg_fitness:.1e}:{cur_max_fitness:.1e}) - Apple ({cur_min_apple_eaten}:{round(cur_avg_apple_eaten, 1)}:{cur_max_apple_eaten}) - Best snake {max_snake_length}"

    if c.DISPLAY_GRAPHICS:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        pygame.display.set_caption(info)

        if not c.DISPLAY_ALL_POPULATION:
            for (x, y) in game.snake_body:
                pygame.draw.circle(screen, "darkolivegreen3", (x * CELL_SIDE + CELL_SIDE / 2, y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 2)
            (x, y) = game.snake_body[0] # head of the snake
            pygame.draw.circle(screen, "black", (x * CELL_SIDE + CELL_SIDE / 2, y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 4)
            (x, y) = game.apple
            pygame.draw.circle(screen, "brown3", (x * CELL_SIDE + CELL_SIDE / 2, y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 2)
            # surround the current game with a black rectangle
            pygame.draw.rect(screen, "black", (BOARD_WIDTH, BOARD_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT), 1)
        else:
            # draw all games of the game collection in one big table and each game has coordinate and use a square matrix of sqrt(POPULATION) x sqrt(POPULATION)
            # Iterate over each game in the collection
            for i, game in enumerate(game_collection.games):
                # Calculate the row and column of the current game in the table
                row = i // games_per_side
                col = i % games_per_side

                # if game is lost change the color of the rectangle to red
                if game.lost:
                    pygame.draw.rect(screen, "red", (col * GAME_WIDTH, row * GAME_HEIGHT, GAME_WIDTH, GAME_HEIGHT))

                # do a case switch to change the color of the rectangle depending on the death reason
                if game.death_reason == "Wall":
                    pygame.draw.rect(screen, "orange", (col * GAME_WIDTH, row * GAME_HEIGHT, GAME_WIDTH, GAME_HEIGHT))
                elif game.death_reason == "Body":
                    pygame.draw.rect(screen, "blue", (col * GAME_WIDTH, row * GAME_HEIGHT, GAME_WIDTH, GAME_HEIGHT))
                elif game.death_reason == "Life":
                    pygame.draw.rect(screen, "green", (col * GAME_WIDTH, row * GAME_HEIGHT, GAME_WIDTH, GAME_HEIGHT))

                # surround the current game with a black rectangle
                pygame.draw.rect(screen, "black", (col * GAME_WIDTH, row * GAME_HEIGHT, GAME_WIDTH, GAME_HEIGHT), 1)

                # Calculate the position of the game cell on the screen
                cell_x = col * GAME_WIDTH
                cell_y = row * GAME_HEIGHT

                # Draw the game on the screen at the calculated position
                for (x, y) in game.snake_body:
                    pygame.draw.circle(screen, "darkolivegreen3", (cell_x + x * CELL_SIDE + CELL_SIDE / 2, cell_y + y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 2)
                (x, y) = game.snake_body[0]
                pygame.draw.circle(screen, "black", (cell_x + x * CELL_SIDE + CELL_SIDE / 2, cell_y + y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 4)
                (x, y) = game.apple
                pygame.draw.circle(screen, "brown3", (cell_x + x * CELL_SIDE + CELL_SIDE / 2, cell_y + y * CELL_SIDE + CELL_SIDE / 2), CELL_SIDE / 2)

            # zoom on longest snake
            game, current_snake = game_collection.longest_snake() # to see the longest snake
            row = current_snake // games_per_side
            col = current_snake % games_per_side
            cell_x = col * GAME_WIDTH
            cell_y = row * GAME_HEIGHT
            # draw a white rectangle centred on (cell_x, cell_y) with a width of c.ZOOM_FACTOR * WIDTH + CELL_SIDE and a height of c.ZOOM_FACTOR * HEIGHT + CELL_SIDE
            pygame.draw.rect(screen, "yellow", (cell_x, cell_y, c.ZOOM_FACTOR * GAME_WIDTH, c.ZOOM_FACTOR * GAME_HEIGHT))
            for (x, y) in game.snake_body:
                pygame.draw.circle(screen, "darkolivegreen3", (cell_x + c.ZOOM_FACTOR * (x + CELL_SIDE + CELL_SIDE / 2), cell_y + c.ZOOM_FACTOR * (y * CELL_SIDE + CELL_SIDE / 2)), c.ZOOM_FACTOR * CELL_SIDE / 2)
            (x, y) = game.snake_body[0]
            pygame.draw.circle(screen, "black", (cell_x + c.ZOOM_FACTOR * (x + CELL_SIDE + CELL_SIDE / 2), cell_y + c.ZOOM_FACTOR * (y * CELL_SIDE + CELL_SIDE / 2)), c.ZOOM_FACTOR * CELL_SIDE / 4)
            (x, y) = game.apple
            pygame.draw.circle(screen, "brown3", (cell_x + c.ZOOM_FACTOR * (x + CELL_SIDE + CELL_SIDE / 2), cell_y + c.ZOOM_FACTOR * (y * CELL_SIDE + CELL_SIDE / 2)), c.ZOOM_FACTOR * CELL_SIDE / 2)
    else:
        print(info)


    # update your game state here
    if not game_collection.step(c.LIFE_TIME): # all sakes in collection dead go next iteration
        max_fitness.append(cur_max_fitness)
        min_fitness.append(cur_min_fitness)
        avg_fitness.append(cur_avg_fitness)
        max_apple_eaten.append(cur_max_apple_eaten)
        min_apple_eaten.append(cur_min_apple_eaten)
        avg_apple_eaten.append(cur_avg_apple_eaten)
        # plot max_fitness as function of 0:iteration
        iteration += 1
        if iteration >= c.MAX_ITERATION:
            break

    if c.DISPLAY_GRAPHICS:
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(500)

if c.SAVE:
    game_collection.save_brains(c.BRAINS_FILE)
    save_curves(c.CURVES_FILES)

print(max_fitness)

fig, ax1 = plt.subplots()

color1 = 'tab:blue'
color2 = 'tab:red'
color3 = 'tab:green'
color4 = 'tab:orange'

ax1.set_xlabel('Génération')
ax1.set_ylabel('Fitness maximum', color=color1)
ax1.set_yscale('log')

# Key change: Use iterations as the x-axis data
ax1.plot(range(len(max_fitness)), max_fitness, color=color2, label='Fitness max')
ax1.plot(range(len(avg_fitness)), avg_fitness, color=color1, label='Fitness avg')
ax1.tick_params(axis='y', labelcolor=color1)

ax1.legend(loc='upper left')  # Add a legend for clarity

color3 = 'tab:green'
ax2 = ax1.twinx()
ax2.set_ylabel('Pommes mangées maximum', color=color3)
# Key change: Use iterations as the x-axis data
ax2.plot(range(len(max_apple_eaten)), max_apple_eaten, color=color4, label='Pommes')
ax2.tick_params(axis='y', labelcolor=color3)

ax2.legend(loc='lower right')

# Add Vertical Gridlines (The Key Change)
ax1.grid(axis='x', linestyle='--')  # Gridlines on the x-axis (iterations)
ax2.grid(axis='y', linestyle='--')  # You need to add it for the second axis too

# Additional styling improvement
plt.title('Fitness et pommes mangées fct. nombre de générations')
fig.tight_layout()

plt.show()

if c.DISPLAY_GRAPHICS:
    pygame.quit()
