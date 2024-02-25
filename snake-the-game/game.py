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

    apples_eaten = 0
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # Neural network composed of 4 layers, input layer has 24 neurons, 2 hidden layers each with 18 neurons, output layer has 4 neurons (4 directions)
        # in total it has 24 + 18 + 18 + 4 = 64 neurons.
        self.brain = NeuralNetwork.random([24, 18, 18, 4])
    
    def step(self) -> bool:
        # process the vision output through the neural network and output activation
        activation = self.brain.feedforward(self.process_vision())
        # take the highest activation index for the direction to take
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

        #collisions avec le corps
        for bit in self.snake_body[1:]:
            if bit == self.snake_body[0]:
                self.lost = True
                return False
            
        #collisions avec la pomme
        if self.snake_body[0] == self.apple:
            self.snake_body.append(end_tail)
            self.apple = (randrange(0, self.width), randrange(0, self.height))
            self.apples_eaten += 1

        return True
    

    def process_vision(self) -> [float]:
        vision = [0 for _ in range(3*8)]
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for (i, incrementer) in enumerate(directions):
            apple_distance = -1
            wall_distance = -1
            tail_distance = -1

            (x, y) = self.snake_body[0]
            distance = 0

            while True:
                x += incrementer[0]
                y += incrementer[1]
                distance += 1

                # sortie de grille
                if x < 0 or x >= self.width or y < 0 or y >= self.height:
                    wall_distance = distance
                    break

                # sur la pomme
                if (x, y) == self.apple and apple_distance == -1:
                    apple_distance = distance

                # sur la queue
                if (x, y) in self.snake_body and tail_distance == -1:
                    tail_distance = distance

            vision[3*i] = 0 if apple_distance == -1 else 1
            vision[3*i + 1] = 1 / wall_distance
            vision[3*i + 2] = tail_distance if tail_distance != -1 else 0


        return vision
    
    def fitness(self, age):
        return (age * age) * pow(2, self.apples_eaten) * (100 * self.apples_eaten + 1)
        # return (age * age * age * age) * pow(2, self.apples_eaten) * (500 * self.apples_eaten + 1)
    # age to the power of 4 vs 3 vs 2