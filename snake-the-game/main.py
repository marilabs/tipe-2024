import pygame
from random import randrange
from game import Game

# game = Game()

from game_collection import GameCollection

game_collection = GameCollection(100)

SIDE = 50
WIDTH = 20
HEIGHT = 15

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH * SIDE, HEIGHT * SIDE))
clock = pygame.time.Clock()
running = True
dt = 0

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
        pygame.draw.circle(screen, "green", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)

    (x, y) = game.snake_body[0]
    pygame.draw.circle(screen, "black", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 4)

    (x, y) = game.apple
    pygame.draw.circle(screen, "red", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)


    # pygame.draw.circle(screen, "red", player_pos, 40)

    # update your game state here

    running = running and game_collection.step()

    # flip() the display to put your work on screen
    pygame.display.flip()
    print(running)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    # dt = clock.tick(60) / 1000
    clock.tick(3)

pygame.quit()