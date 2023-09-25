# un seul serpent

from random import randrange
from neural_network import NeuralNetwork
from numpy import argmax

class Game:
    width = 20
    height = 15
    snake_body = [
        (int(width / 2), int(height / 2)),
            (int(width / 2) + 1, int(height / 2)), 
            (int(width / 2) + 2, int(height / 2))
        ]
    apple = (randrange(0, width), randrange(0, height))

    lost = False

    direction = (-1, 0)

    brain = NeuralNetwork()

    '''def step(self) -> bool:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction = (1, 0)
        elif keys[pygame.K_UP]:
            self.direction = (0, -1)
        elif keys[pygame.K_LEFT]:
            self.direction = (-1, 0)
        elif keys[pygame.K_DOWN]:
            self.direction = (0, 1)

        return self.move_snake(self.direction)'''
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.snake_body = [
        (int(width / 2), int(height / 2)),
            (int(width / 2) + 1, int(height / 2)), 
            (int(width / 2) + 2, int(height / 2))
        ]
    
    def step(self) -> bool:
        activation = self.brain.feedforward([0.0 for _ in range(18)])
        index = argmax(activation)

        match index:
            case 0:
                self.direction = (1, 0)
            case 1:
                self.direction = (0, -1)
            case 2:
                self.direction = (-1, 0)
            case 3:
                self.direction = (0, 1)

        
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction = (1, 0)
        elif keys[pygame.K_UP]:
            self.direction = (0, -1)
        elif keys[pygame.K_LEFT]:
            self.direction = (-1, 0)
        elif keys[pygame.K_DOWN]:
            self.direction = (0, 1)'''

        return self.move_snake(self.direction)


    def move_snake(self, incrementer: (int, int)) -> bool:
        moved_head = (self.snake_body[0][0] + incrementer[0], self.snake_body[0][1] + incrementer[1])
        # vérification de la présence de la tête dans la grille
        if not (0 <= moved_head[0] < self.width and 0 <= moved_head[1] < self.height):
            self.lost = True
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
                self.lost = True
                return False
            
        #collisions avec la pomme
        if self.snake_body[0] == self.apple:
            self.snake_body.append(end_tail)
            self.apple = (randrange(0, self.width), randrange(0, self.height))

        return True