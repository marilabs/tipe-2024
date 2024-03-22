DEBUG = False
ORIGINAL_SIZE_THREE = True
DISPLAY_ALL_POPULATION = True

DISPLAY_LARGEST_SNAKE = False

# number of cells for the snake to move in each game
WIDTH = 10
HEIGHT = 10

BOARD_SIDE = 880 # indication of largest board side (for max of WIDTH and HEIGHT)
NUMBER_GAMES = 22**2 # 484 number of games in the collection -> number of snakes in parallel
ZOOM_FACTOR = 2 # zoom factor for the longuest snake

MAX_ITERATION = 2000 # number of iterations before stopping the program
RESTORE = True # restore the game brains from a file
BRAINS_FILE = 'saved_brains.pickle' # name of the file to save the brains
#BRAINS_FILE = 'saved_brains.pickle' + '-' + NUMBER_GAMES # name of the file to save the brains

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

