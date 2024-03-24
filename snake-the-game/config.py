DEBUG = False
ORIGINAL_SIZE_THREE = True
DISPLAY_ALL_POPULATION = True

DISPLAY_LARGEST_SNAKE = False

DISPLAY_GRAPHICS = False

# number of cells for the snake to move in each game
WIDTH = 10
HEIGHT = 10

BOARD_SIDE = 880 # indication of largest board side (for max of WIDTH and HEIGHT)
POPULATION = 22**2 # 484 population of snakes or number of games in the collection
ZOOM_FACTOR = 2 # zoom factor for the longuest snake

MAX_ITERATION = 500 # number of iterations before stopping the program
SAVE = True # save the game brains to a file
RESTORE = True # restore the game brains from a file
BRAINS_FILE = 'saved_brains.pickle' + '-' + str(POPULATION) # name of the file to save the brains

#! check https://craighaber.github.io/AI-for-Snake-Game/website_files/index.html code 0.08 and k?
NUMBER_CROSSOVER_POINTS = 4 # number of crossover points for the genetic algorithm
MUTATION_CHANCE = 0.5 # chance of mutation for the genetic algorithm
MUTATION_COEFF = 0.5 # coefficient for the mutation
PORTION_BESTS = 50 # percentage of bests brains to keep for the genetic algorithm

LIFE_TIME = True # apply life time constraint to the snake to avoid infinite loops
MAX_LIFE_POINTS = 50 # maximum number of life points for the snake
APPLE_LIFETIME_GAIN = 20 # number of life points gained when eating an apple

SINGLE_SNAKE_BRAIN = 1 # number of snakes in the single snake game

up = (0, 1);
down = (0, -1)
left = (-1, 0)
right = (1, 0)
up_right = (1, 1)
up_left = (-1, 1)
down_left = (-1, -1)
down_right = (1, -1)
eight_directions = [right, up_right, up, up_left, left, down_left, down, down_right]
four_directions = [right, up, left, down]
