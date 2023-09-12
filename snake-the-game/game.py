# un seul serpent

from random import randrange
import pygame

class Game:
    WIDTH = 20
    HEIGHT = 15
    snake_body = [
        (int(WIDTH / 2), int(HEIGHT / 2)),
            (int(WIDTH / 2) + 1, int(HEIGHT / 2)), 
            (int(WIDTH / 2) + 2, int(HEIGHT / 2))
        ]
    apple = (randrange(0, WIDTH), randrange(0, HEIGHT))

    direction = (-1, 0)

    def step(self) -> bool:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction = (1, 0)
        elif keys[pygame.K_UP]:
            self.direction = (0, -1)
        elif keys[pygame.K_LEFT]:
            self.direction = (-1, 0)
        elif keys[pygame.K_DOWN]:
            self.direction = (0, 1)


    def move_snake(self, incrementer: (int, int)) -> bool:

        moved_head = (self.snake_body[0][0] + incrementer[0], self.snake_body[0][1] + incrementer[1])
        # vérification de la présence de la tête dans la grille
        if not (0 <= moved_head[0] < self.WIDTH and 0 <= moved_head[1] < self.HEIGHT):
            return False
        
        # sauvegarde de la fin de la queue
        end_tail = self.snake_body[-1]
        
        # déplacement du serpent
        for i in reversed(range(1, len(self.snake_body))):
            self.snake_body[i] = self.snake_body[i - 1]
        
        self.snake_body[0] = moved_head

        #collisions avec la corps
        for bit in self.snake_body[1:]:
            if bit == self.snake_body[0]:
                return False
            
        #collisions avec la pomme
        if self.snake_body[0] == self.apple:
            self.snake_body.append(end_tail)
            self.apple = (randrange(0, self.WIDTH), randrange(0, self.HEIGHT))

        return True