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

game_collection = GameCollection(c.POPULATION, c.WIDTH, c.HEIGHT)

if c.RESTORE and os.path.exists(c.BRAINS_FILE):
    game_collection.restore_brains(c.BRAINS_FILE)

# pygame setup
pygame.init()

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

screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

clock = pygame.time.Clock()
running = True
dt = 0

def save_and_exit(signal, frame):
    game_collection.save_brains(c.BRAINS_FILE)
    sys.exit(0)

# save program state in case of interruption
signal.signal(signal.SIGINT, save_and_exit)

iteration = 0

max_fitness = []
avg_fitness = []
max_apple_eaten = []
max_snake_length = 0

#? VERIFIED
while running:

    cur_max_fitness = game_collection.best_fitness()
    cur_avg_fitness = game_collection.average_fitness()
    cur_max_apple_eaten = game_collection.max_apple_eaten()
    if cur_max_apple_eaten >= max_snake_length:
        max_snake_length = cur_max_apple_eaten + 1

    # retrieve the new game
    if c.DISPLAY_LARGEST_SNAKE:
        game, current_snake = game_collection.longest_snake() # to see the longest snake
    else:
        game, current_snake = game_collection.snake_to_display()

    # display game iteration and fitness of the game (generation) as window title
    info = f"Gen {game_collection.generation} - Iter {game_collection.iteration} - Fitness {game.fitness():.2e} - Max fitness {cur_max_fitness:.2e} - Avg fitness {round(cur_avg_fitness, 2):.2e} - Max eaten {cur_max_apple_eaten} - Longest ever {max_snake_length}"
    
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
            # suround the current game with a black rectangle
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

                # suround the current game with a black rectangle
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
            # draw a white rectangle centered on (cell_x, cell_y) with a width of c.ZOOM_FACTOR * WIDTH + CELL_SIDE and a height of c.ZOOM_FACTOR * HEIGHT + CELL_SIDE
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
    if not game_collection.step(): # all sakes in collection dead go next iteration
        max_fitness.append(cur_max_fitness)
        avg_fitness.append(cur_avg_fitness)
        max_apple_eaten.append(cur_max_apple_eaten)
        # plot max_fitness as function of 0:interation
        iteration += 1
        if iteration >= c.MAX_ITERATION:
            break

    if c.DISPLAY_GRAPHICS:
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(500)

game_collection.save_brains(c.BRAINS_FILE)

print(max_fitness)

"""
# Set the y-axis limits from 0 to max_fitness_value
plt.plot(range(len(max_fitness)), max_fitness, color='blue', label='Max Fitness')
plt.plot(range(len(max_fitness)), avg_fitness, color='green', label='Average Fitness')
plt.plot(range(len(max_fitness)), max_apple_eaten, color='red', label='Max Apples Eaten')

plt.xlabel('Iteration')
plt.ylabel('Fitness')
plt.ylim(0, max(np.max(max_fitness), np.max(avg_fitness), np.max(max_apple_eaten)))
plt.title('Fitness vs Iteration')
plt.grid(True)
plt.legend()
plt.show()
"""

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Iteration')
ax1.set_ylabel('Max Fitness', color=color)
#x_new = np.linspace(0, len(max_fitness), 300)
#spl = make_interp_spline(range(len(max_fitness)), max_fitness, k=3)
#max_fitness_smooth = spl(x_new)
#ax1.plot(x_new, max_fitness_smooth, color=color)
ax1.set_yscale('log')
ax1.plot(range(len(max_fitness)), max_fitness, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Average Fitness', color=color)
ax2.set_yscale('log')
ax2.plot(range(len(avg_fitness)), avg_fitness, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  
plt.title('Max and Average Fitness vs Iteration')
plt.grid(True)
plt.show()

"""
fig, ax1 = plt.subplots()

color1 = 'tab:blue'
ax1.set_xlabel('Iteration')
ax1.set_ylabel('Max Fitness', color=color1)
ax1.plot(range(len(max_fitness)), max_fitness, color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

color2 = 'tab:red'
ax2 = ax1.twinx()  
ax2.set_ylabel('Average Fitness', color=color2)
ax2.plot(range(len(avg_fitness)), avg_fitness, color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

color3 = 'tab:green'
ax1.plot(range(len(max_apple_eaten)), max_apple_eaten, color=color3, linestyle='dashed', label='Max Apples Eaten')

fig.tight_layout()  
plt.title('Fitness vs Iteration')
plt.grid(True)
plt.show()
"""

pygame.quit()
