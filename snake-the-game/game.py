# un jeu = un seul serpent

from random import randrange
from neural_network import NeuralNetwork
from numpy import argmax
import collections
import config as c
from typing import Tuple, List
import math

class Game:

    vision = []

    def __init__(self, width: int = 10, height: int = 10, max_life_points: int = 50, apple_lifetime_gain: int = 500, strategy: int = 2, num_fitness: int = 1) -> None:
        self.width = width
        self.height = height
        self.max_life_points = max_life_points
        self.apple_lifetime_gain = apple_lifetime_gain
        self.strategy = strategy
        self.last_space = 0
        self.last_visited = set()

        """
        Various rules to create a neural network:
        * The number of hidden neurons should be between the size of the input layer and the size of the output layer.
        * The number of hidden neurons should be 2/3 the size of the input layer, plus the size of the output layer.
        * The number of hidden neurons should be less than twice the size of the input layer.
        * The number of hidden neurons should be between the size of the input layer and the output layer.
        * The most appropriate number of hidden neurons is sqrt(input layer nodes * output layer nodes)
        """

        if strategy == 1:
            # Neural network composed of 4 layers, input layer has 24 neurons, 2 hidden layers each with 18 neurons, output layer has 4 neurons (4 directions)
            # in total it has 24 + 18 + 18 + 4 = 64 neurons.
            self.brain = NeuralNetwork([24, 18, 18, 4])
            self.vision_strategy = self.process_vision
        elif strategy == 2:
            self.brain = NeuralNetwork([9, 10, 10, 4])
            self.vision_strategy = self.process_vision2
        elif strategy == 3:
            self.brain = NeuralNetwork([13, 12, 12, 4])
            self.vision_strategy = self.process_vision3
        elif strategy == 4:
            self.brain = NeuralNetwork([25, 18, 18, 4])
            self.vision_strategy = self.process_vision4
        elif strategy == 5:
            self.brain = NeuralNetwork([13, 12, 12, 4])
            self.vision_strategy = self.process_vision5

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
        self.seed_new_apple()
        self.life_points = self.max_life_points
        self.died_bc_no_apple = 0
        self.death_reason = "None"
        if c.NORMALIZE_BOARD:
            self.norm_constant_diag = math.sqrt(width ** 2 + height ** 2)
            self.norm_constant_board = width * height / 10.0
        else:
            self.norm_constant_diag = 1
            self.norm_constant_board = 20.0

        if num_fitness == 1:
            self.fitness = self.fitness1
        elif num_fitness == 2:
            self.fitness = self.fitness2
        elif num_fitness == 3:
            self.fitness = self.fitness3
        elif num_fitness == 4:
            self.fitness = self.fitness4
        elif num_fitness == 5:
            self.fitness = self.fitness5

    def seed_new_apple(self):
        self.apple = (randrange(0, self.width), randrange(0, self.height))
        while self.apple in self.snake_body:
            self.apple = (randrange(0, self.width), randrange(0, self.height))

    def step(self, life_time: bool) -> bool:
        # process the vision output through the neural network and output activation
        activation = self.brain.feedforward(self.vision_strategy())
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
            self.seed_new_apple()
            self.apples_eaten += 1
            if c.RESET_LIFETIME:
                self.life_points = self.max_life_points # on réinitialise la durée de vie au max
            else:
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
            # optimize not to recalculate last_visited and last_space for strategy 2
            # if moved_head is in last_visited it needs to be removed since the snake has its head there now
            if self.strategy == 2  or self.strategy == 5: # update last_visited and last_space
                if moved_head in self.last_visited: # adapt last_visited and last_space
                    self.last_visited.remove(moved_head) # only head is to be removed since tail not moved with apple eaten
                    self.last_space -= 1
                else: # reset last_visited and last_space
                    self.last_space = 0
                    self.last_visited = set()
        else:
            # optimize not to recalculate last_visited and last_space for strategy 2
            if self.strategy == 2 or self.strategy == 5: # update last_visited and last_space
                if moved_head in self.last_visited: # adapt last_visited and last_space
                    self.last_visited.remove(moved_head) # only head is to be removed since tail not moved with apple eaten
                    self.last_space -= 1
                    # check if end_tail is connected to last_visited elements (can be visited) since it has moved and leaves an empty space
                    if any(abs(end_tail[0] - x) == 1 ^ abs(end_tail[1] - y) == 1 for (x, y) in self.last_visited):
                        self.last_visited.add((end_tail[0], end_tail[1]))
                        self.last_space += 1
                else: # reset last_visited and last_space
                    self.last_space = 0
                    self.last_visited = set()

        # vérification de la durée de vie
        if life_time and self.life_points <= 0:
            self.death_reason = "Life"
            self.lost = True
            self.died_bc_no_apple = 1
            return False

        return True

    # vision strategy: 8 directions, 3 informations per direction
    # (1D distance to apple in direction of move, 1 / wall_distance in direction of move, tail_distance in direction of move) + apples_eaten + original_size
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

        self.vision = vision
        return vision

    # vision strategy: 4 directions, 3 informations per direction
    # (manhattan distance to apple, 1 / wall_distance in direction of move, tail_distance in direction of move) + apples_eaten + original_size
    def process_vision3(self) -> List[float]:
        vision = []

        for (i, incrementer) in enumerate(c.four_directions):
            apple_distance = -1
            wall_distance = -1
            tail_distance = -1

            (x, y) = self.snake_body[0]
            distance = 0

            # try to get inputs between [0,1] for the neural network

            distance_apple = self.manhattan_distance_to_apple((x + incrementer[0], y + incrementer[1]))

            vision.append(1.0 / distance_apple if distance_apple != 0 else 1)

            while True:
                x += incrementer[0]
                y += incrementer[1]
                distance += 1

                # sortie de grille
                if not self.is_on_board(x, y):
                    wall_distance = distance
                    break

                # sur la queue
                if (x, y) in self.snake_body and tail_distance == -1:
                    tail_distance = distance

            vision.append(1.0 / wall_distance)
            vision.append(1.0 / tail_distance if tail_distance != -1 else 1)

        vision.append(1 / (self.apples_eaten + self.original_size))

        self.vision = vision
        return vision

    # vision strategy: 4 directions, 3 informations per direction
    # (1 if direction is the closest to the apple, 1 / wall_distance in direction of move, tail_distance in direction of move) + apples_eaten + original_size
    def process_vision4(self) -> List[float]:
        vision = []

        min_distance_index = min(range(len(c.eight_directions)), key=lambda i: self.manhattan_distance_to_apple((self.snake_body[0][0] + c.eight_directions[i][0], self.snake_body[0][1] + c.eight_directions[i][1])))

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

                # sur la queue
                if (x, y) in self.snake_body and tail_distance == -1:
                    tail_distance = distance

            vision.append(1 if i == min_distance_index else 0)
            vision.append(1.0 / wall_distance)
            vision.append(tail_distance if tail_distance != -1 else 0)

        vision.append(self.apples_eaten + self.original_size)
        self.vision = vision
        return vision

    #? weights 8 bits vs. float? normalization?

    # vision strategy: 4 directions, 3 informations per direction
    # (free spaces in direction of move, manhattan distance to apple in direction of move, apple is in the free space in this direction) + apples_eaten + original_size
    def process_vision5(self) -> List[float]:
        # neural network input contains free space in all directions, distance to apple in all directions, and number of apples eaten (size of snake)
        # 9 inputs in total
        neural_network_input = []
        (hx, hy) = self.snake_body[0] # head of the snake body
        for direction in c.four_directions:
            (dx, dy) = direction
            (cnx, cny) = (hx + dx, hy + dy)
            #metric = self.count_free_moving_spaces(cnx, cny)
            #neural_network_input.append(1.0 / metric if metric != 0 else 1)
            #metric = self.manhattan_distance_to_apple((cnx, cny))
            #neural_network_input.append(1.0 / metric if metric != 0 else 1)
            neural_network_input.append(self.count_free_moving_spaces(cnx, cny) / self.norm_constant_board)
            neural_network_input.append(self.manhattan_distance_to_apple((cnx, cny)) / self.norm_constant_diag)
            neural_network_input.append(1 if self.apple in self.last_visited else 0) # apple can be reached going in this direction
        #neural_network_input.append(1.0 / (self.apples_eaten + self.original_size))
        neural_network_input.append(self.apples_eaten + self.original_size)
        self.vision = neural_network_input
        return neural_network_input

    # vision strategy: 4 directions, 2 informations per direction
    # (free spaces in direction of move, manhattan distance to apple in direction of move) + apples_eaten + original_size
    def process_vision2(self) -> List[float]:
        # neural network input contains free space in all directions, distance to apple in all directions, and number of apples eaten (size of snake)
        # 9 inputs in total
        neural_network_input = []
        (hx, hy) = self.snake_body[0] # head of the snake body
        for direction in c.four_directions:
            (dx, dy) = direction
            (cnx, cny) = (hx + dx, hy + dy)
            #metric = self.count_free_moving_spaces(cnx, cny)
            #neural_network_input.append(1.0 / metric if metric != 0 else 1)
            #metric = self.manhattan_distance_to_apple((cnx, cny))
            #neural_network_input.append(1.0 / metric if metric != 0 else 1)
            neural_network_input.append(self.count_free_moving_spaces(cnx, cny) / self.norm_constant_board)
            neural_network_input.append(self.manhattan_distance_to_apple((cnx, cny)) / self.norm_constant_diag)
        #neural_network_input.append(1.0 / (self.apples_eaten + self.original_size))
        neural_network_input.append(self.apples_eaten + self.original_size)
        self.vision = neural_network_input
        return neural_network_input

    def is_on_board(self, x, y) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_possible_move(self, x, y) -> bool:
        # check if the move is on the board and not on the snake body except for the tail (since it has moved)
        return self.is_on_board(x, y) and (x, y) not in self.snake_body[:-1]

    def get_possible_moves(self, cur):
        (x, y) = cur
        moves = []
        for direction in c.eight_directions:
            (i, j) = direction
            if self.is_possible_move(x + i, y + j):
                moves.append(direction)
        return moves

    #! todo: understand why changing fitness it is nok for previous brains...
    #! todo: play with fitness and understand the impact on the game

    def count_free_moving_spaces(self, x, y) -> int:
        # Breadth-First Search, BFS, snake heads moves to (x, y) and tail's end is no more
        if not self.is_possible_move(x, y): # does not check snake's tail
            return 0
        if (x, y) in self.last_visited:
            return self.last_space
        space = 0
        visited = set([(x, y)])
        queue = collections.deque([(x, y)]) # efficient for pop(0) and append
        while (len(queue) > 0):
            cur = queue.popleft()
            space += 1
            for direction in self.get_possible_moves(cur):
                (i, j) = direction
                (cx, cy) = cur
                cn = (cx + i, cy + j)
                (cnx, cny) = cn
                if cn not in visited and self.is_possible_move(cnx, cny): # does not check snake's tail
                    queue.append(cn)
                    visited.add(cn)
        self.last_visited = visited
        self.last_space = space
        return space

    def manhattan_distance_to_apple(self, head):
        return abs(self.apple[0] - head[0]) + abs(self.apple[1] - head[1])

    def fitness1(self):
        return pow(3, self.apples_eaten) * (self.age - 50 * self.died_bc_no_apple)

    def fitness2(self):
        return (self.apples_eaten ** 3) * (self.age - 50 * self.died_bc_no_apple)

    def fitness3(self):
        return ((self.apples_eaten * 2) ** 2) * ((self.age - 50 * self.died_bc_no_apple) ** 1.5)

    def fitness4(self):
        return (self.age * self.age) * pow(2, self.apples_eaten) * (100 * self.apples_eaten + 1)

    def fitness5(self):
        return (self.age * self.age * self.age * self.age) * pow(2, self.apples_eaten) * (500 * self.apples_eaten + 1)

    # age^2*2^apple*(coeff*apple+1)
    # age^2*2^10*(apple-9)*(coeff*10)

    # score = self.apples_eaten, frame_score = self.age
    # ((score^3)*(frame_score)
    # ((score*2)^2)*(frame_score^1.5)

    # remarks
    # * 3^apple*(age): pow(3, self.apples_eaten) * (self.age - 50 * self.died_bc_no_apple) trains faster
