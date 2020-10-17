from math import sin

from neat.activations import Tanh
from neat.crossovers import StandardCrossover
from neat.generators import UniformGenerator
from neat.genetic_algorithm import GeneticAlgorithm
from neat.mutations import UniformWeightMutation, AddConnectionMutation, AddNodeMutation


ACTIVATION = Tanh()

MIN_BIAS = -0.1
MAX_BIAS = 0.1

WEIGHT_MUTATION_PROBABILITY = 0.8
PERTURBING_PROBABILITY = 0.99
PERTURBING_MIN = -0.2
PERTURBING_MAX = 0.2

ADD_CONNECTION_PROBABILITY = 0.15
MIN_WEIGHT = -1.0
MAX_WEIGHT = 1.0

ADD_NODE_PROBABILITY = 0.13
NEW_WEIGHT = 1.0

CROSSOVER_PROBABILITY = 0.9
DISABLE_CONNECTION_PROBABILITY = 0.15

POPULATION_SIZE = 100
MAX_GENERATIONS = 300
SAVE_BEST_COUNT = 0

C1 = 1.0
C2 = 1.0
C3 = 1.5
N = 1
DT = 3.0


class SineTestNeat(GeneticAlgorithm):

    def __init__(self,
                 input_dim,
                 output_dim,
                 fitness_calculator):
        super().__init__(
            fitness_calculator=fitness_calculator,
            generator=UniformGenerator(input_dim, output_dim, ACTIVATION, MIN_BIAS, MAX_BIAS),
            mutations=[
                (UniformWeightMutation(PERTURBING_PROBABILITY, PERTURBING_MIN, PERTURBING_MAX, MIN_WEIGHT, MAX_WEIGHT),
                 WEIGHT_MUTATION_PROBABILITY),
                (AddConnectionMutation(MIN_WEIGHT, MAX_WEIGHT), ADD_CONNECTION_PROBABILITY),
                (AddNodeMutation(ACTIVATION, MIN_BIAS, MAX_BIAS, NEW_WEIGHT), ADD_NODE_PROBABILITY)
            ],
            crossover=(StandardCrossover(DISABLE_CONNECTION_PROBABILITY), CROSSOVER_PROBABILITY),
            population_size=POPULATION_SIZE,
            max_generations=MAX_GENERATIONS,
            save_best_count=SAVE_BEST_COUNT,
            c1=C1,
            c2=C2,
            c3=C3,
            n=N,
            dt=DT
        )


min_x = -3
max_x = 3
step = 0.1

current = min_x
pairs = []
while current < max_x:
    pairs.append((current, sin(current)))
    current += step


def calculate_mse(f, verbose=False):
    mse = 0
    for x, y in pairs:
        output = f([x])[0]
        diff = output - y
        mse += diff ** 2

        if verbose:
            print(f"x = {x}, y = {y}, f = {output}, difference={diff}")

    return len(pairs) / mse


neat = SineTestNeat(1, 1, calculate_mse)
best_function = neat.optimize()
calculate_mse(best_function, verbose=True)
