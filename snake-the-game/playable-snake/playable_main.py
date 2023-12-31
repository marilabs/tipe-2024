# Example file showing a circle moving on screen
import pygame
from random import randrange
from playable_game import Game

game = Game()

SIDE = 50

# pygame setup
pygame.init()
screen = pygame.display.set_mode((game.WIDTH * SIDE, game.HEIGHT * SIDE))
clock = pygame.time.Clock()
running = True
dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

"""apple = (randrange(0, game.WIDTH), randrange(0, game.HEIGHT))

snake_body = [(int(game.WIDTH / 2), int(game.HEIGHT / 2)),
            (int(game.WIDTH / 2) + 1, int(game.HEIGHT / 2)), 
            (int(game.WIDTH / 2) + 2, int(game.HEIGHT / 2))]"""

direction = (-1, 0)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("darkolivegreen3")

    for (x, y) in game.snake_body:
        pygame.draw.circle(screen, "darkolivegreen4", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)

    (x, y) = game.snake_body[0]
    pygame.draw.circle(screen, "black", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 4)

    (a, b) = game.apple
    pygame.draw.circle(screen, "brown3", (a * SIDE + SIDE/2, b * SIDE + SIDE/2), SIDE / 2)


    # pygame.draw.circle(screen, "red", player_pos, 40)

    # update your game state here

    running = running and game.step()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    # dt = clock.tick(60) / 1000
    clock.tick(3)

pygame.quit()