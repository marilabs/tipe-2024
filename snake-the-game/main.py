import pygame
from random import randrange
from game import Game

game = Game()

SIDE = 50

# pygame setup
pygame.init()
screen = pygame.display.set_mode((game.WIDTH * SIDE, game.HEIGHT * SIDE))
clock = pygame.time.Clock()
running = True
dt = 0

apple = (randrange(0, game.WIDTH), randrange(0, game.HEIGHT))

snake_body = [(int(game.WIDTH / 2), int(game.HEIGHT / 2)),
            (int(game.WIDTH / 2) + 1, int(game.HEIGHT / 2)), 
            (int(game.WIDTH / 2) + 2, int(game.HEIGHT / 2))]

direction = (-1, 0)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for (x, y) in snake_body:
        pygame.draw.circle(screen, "green", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)

    (x, y) = snake_body[0]
    pygame.draw.circle(screen, "black", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 4)

    (x, y) = apple
    pygame.draw.circle(screen, "red", (x * SIDE + SIDE/2, y * SIDE + SIDE/2), SIDE / 2)


    # pygame.draw.circle(screen, "red", player_pos, 40)

    # update your game state here

    running = running and game.setp()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    # dt = clock.tick(60) / 1000
    clock.tick(3)

pygame.quit()