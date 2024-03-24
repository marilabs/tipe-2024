# un jeu = un seul serpent

from random import randrange
from neural_network import NeuralNetwork
from numpy import argmax
import collections
import config as c
from typing import Tuple, List

class Game:

    def __init__(self, width: int = 10, height: int = 10, max_life_points: int = 50, apple_lifetime_gain: int = 500) -> None:
        self.width = width
        self.height = height
        self.max_life_points = max_life_points
        self.apple_lifetime_gain = apple_lifetime_gain

        # The number of hidden neurons should be between the size of the input layer and the size of the output layer.
        # The number of hidden neurons should be 2/3 the size of the input layer, plus the size of the output layer.
        # The number of hidden neurons should be less than twice the size of the input layer.

        # The number of hidden neurons should be between the size of the input layer and the output layer.
        # The most appropriate number of hidden neurons is sqrt(input layer nodes * output layer nodes)

        # Neural network composed of 4 layers, input layer has 24 neurons, 2 hidden layers each with 18 neurons, output layer has 4 neurons (4 directions)
        # in total it has 24 + 18 + 18 + 4 = 64 neurons.
        # for process_vision() the input is 24 neurons, for process_vision2() the input is 8 neurons (3*8 = 24 neurons)
        self.brain = NeuralNetwork([24, 18, 18, 4]) # hidden layer 24/3+4 = 12 neurons
        #self.brain = NeuralNetwork([9, 10, 10, 4]) # hidden layer 9/3+4 = 7 neurons

        self.apple = (randrange(0, width), randrange(0, height))
        self.age = 0
        self.lost = False
        self.apples_eaten = 0
        #self.direction = (-1, 0) # default direction is left for first move
        self.direction = (randrange(-1, 2), randrange(-1, 2)) # make first move random
        self.snake_body = [ # snake starts at the center and has 3 bits
            (int(width / 2), int(height / 2))
            ]
        if c.ORIGINAL_SIZE_THREE:
            self.snake_body.append((int(width / 2) + 1, int(height / 2)))
            self.snake_body.append((int(width / 2) + 2, int(height / 2))
            )
        self.original_size = len(self.snake_body)
        self.life_points = self.max_life_points
        self.died_bc_no_apple = 0
        self.death_reason = "None"

    def step(self, life_time: bool) -> bool:
        # process the vision output through the neural network and output activation
        #! change vision
        activation = self.brain.feedforward(self.process_vision())
        # take the highest activation index for the direction to take
        index = argmax(activation)

        match index:
            case 0:
                self.direction = c.right
            case 1:
                self.direction = c.up
            case 2:
                self.direction = c.left
            case 3:
                self.direction = c.down

        return self.move_snake(self.direction, life_time)

    def move_snake(self, incrementer: Tuple[int, int], life_time: bool) -> bool:
        moved_head = (self.snake_body[0][0] + incrementer[0], self.snake_body[0][1] + incrementer[1])

        # vérification de la présence de la tête dans la grille
        if not (0 <= moved_head[0] < self.width and 0 <= moved_head[1] < self.height):
            self.death_reason = "Wall"
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
                self.death_reason = "Body"
                return False

        self.age += 1
        self.life_points -= 1

        #collisions avec la pomme
        if self.snake_body[0] == self.apple:
            self.snake_body.append(end_tail) # agrandir le serpent avec la queue précédente
            self.apple = (randrange(0, self.width), randrange(0, self.height)) # nouvelle pomme
            self.apples_eaten += 1
            self.life_points += self.apple_lifetime_gain # on réinitialise la durée de vie conformément au commentaire en dessous:

            """
            The genetic algorithm was run many different times with many different fitness functions.
            Formulaically, the first fitness function was:
            ((score^3)*(frame_score)
            Score is equivalent to the length of the snake minus 1 (since the snake always starts at length 1),
            and frame_score is the amount of frames that the snake was alive. However, originally this fitness
            function resulted in many snakes that looped in circles endlessly without eating any fruit to maximize
            the frame_score component of the function. Thus, the training was modified such that all snakes are
            killed off if they do not eat a fruit in 50 frames. Also, if a snake died due to not eating any fruit
            for 50 frames, 50 points were subtracted from the frame_score to discourage the behaviour.
            """

        # vérification de la durée de vie
        if life_time and self.life_points <= 0:
            self.death_reason = "Life"
            self.lost = True
            self.died_bc_no_apple = 1
            return False

        return True

    def process_vision(self) -> List[float]:
        vision = [0 for _ in range(3*8)]

        for (i, incrementer) in enumerate(c.eight_directions):
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
                if not self.is_on_board(x, y):
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

    #? weights 8 bits vs. float? normalization?

    def process_vision2(self) -> List[float]:
        # neural network input contains free space in all directions, distance to apple in all directions, and number of apples eaten (size of snake)
        # 9 inputs in total
        neural_network_input = []
        constant = 20
        for direction in c.four_directions:
            (dx, dy) = direction
            (hx, hy) = self.snake_body[0] # head of the snake body
            neural_network_input.append(self.count_free_moving_spaces(hx + dx, hy + dy) / constant)
            neural_network_input.append(self.manhattan_distance_to_apple((hx + dx, hy + dy)))
        neural_network_input.append(self.apples_eaten + self.original_size)
        return neural_network_input

    def is_on_board(self, x, y) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_possible_move(self, x, y) -> bool:
        return self.is_on_board(x, y) and (x, y) not in self.snake_body

    def get_possible_moves(self, cur):
        (x, y) = cur
        moves = []
        for direction in c.eight_directions:
            (i, j) = direction
            if self.is_possible_move(x + i, y + j):
                moves.append((x + i, y + j))
        return moves

    def count_free_moving_spaces(self, x, y) -> int:
        if not self.is_possible_move(x, y):
            return 0

        space = 0
        visited = set([x, y])
        queue = collections.deque([(x, y)]) # efficient for pop(0) and append

        while (len(queue) > 0):
            cur = queue.popleft()
            space += 1
            for direction in self.get_possible_moves(cur):
                (i, j) = direction
                if (x + i, y + j) not in visited and self.is_possible_move(x + i, y + j):
                    queue.append((x + i, y + j))
                    visited.add((x + i, y + j))

        return space

    def manhattan_distance_to_apple(self, head):
        return abs(self.apple[0] - head[0]) + abs(self.apple[1] - head[1])

    def fitness(self):
        return pow(3, self.apples_eaten) * (self.age - 50 * self.died_bc_no_apple)
        #return (self.age * self.age) * pow(2, self.apples_eaten) * (100 * self.apples_eaten + 1)
        #return ((self.apples_eaten * 2) ** 2) * (self.age ** 1.5)
        #return (self.age * self.age * self.age * self.age) * pow(2, self.apples_eaten) * (500 * self.apples_eaten + 1)
    # age to the power of 4 vs 3 vs 2
