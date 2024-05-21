DEBUG = False
ORIGINAL_SIZE_THREE = False
DISPLAY_ALL_POPULATION = True

DISPLAY_LARGEST_SNAKE = False

DISPLAY_GRAPHICS = True

# number of cells for the snake to move in each game
WIDTH = 10
HEIGHT = 10

BOARD_SIDE = 880 # indication of largest board side (for max of WIDTH and HEIGHT)
POPULATION = 22**2 # 484 population of snakes or number of games in the collection
ZOOM_FACTOR = 2 # zoom factor for the longest snake

# game strategy, 1:24,18,18,4; 2:9,10,10,4
GAME_STRATEGY = 5
FITNESS_STRATEGY = 3

MAX_ITERATION = 2000 # number of iterations before stopping the program
SAVE = True # save the game brains to a file
RESTORE = True # restore the game brains from a file
BRAINS_FILE = 'saved_brains' + '-' + str(POPULATION) + '-' + str(GAME_STRATEGY) + str(FITNESS_STRATEGY) + '.pickle' # name of the file to save the brains
CURVES_FILES = 'saved_curves' + '-' + str(POPULATION) + '-' + str(GAME_STRATEGY) + str(FITNESS_STRATEGY) + '.pickle' # name of the file to save the curves

NUMBER_CROSSOVER_POINTS = 1 # number of crossover points for the genetic algorithm
MUTATION_CHANCE = 0.1 # chance of mutation for the genetic algorithm
MUTATION_COEFF = 0.1 # coefficient for the mutation
PORTION_BESTS = 10 # percentage of bests brains to keep for the genetic algorithm

# antoine libs/game/lib.rs and game_wasm/src/lib.rs
# k=1 KPointsCrossover
#NUMBER_GAMES: u32 = 2_000; WIDTH: u32 = 30; HEIGHT: u32 = 30;
#MUTATION_CHANCE: f64 = 0.5; MUTATION_COEFF: f32 = 0.5; SAVE_BESTS: usize = 100; MAX_AGE: u32 = 500; APPLE_LIFETIME_GAIN: i32 = 50;

LIFE_TIME = True # apply life time constraint to the snake to avoid infinite loops
MAX_LIFE_POINTS = 50 # maximum number of life points for the snake
APPLE_LIFETIME_GAIN = 20 # number of life points gained when eating an apple
RESET_LIFETIME = True # reset life points when eating an apple
NORMALIZE_BOARD = False

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
