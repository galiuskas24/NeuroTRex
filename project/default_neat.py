from neat.activations import Sigmoid
from neat.crossovers import StandardCrossover
from neat.generators import UniformGenerator
from neat.genetic_algorithm import GeneticAlgorithm
from neat.mutations import UniformWeightMutation, AddConnectionMutation, AddNodeMutation


class NeatSigmoid(Sigmoid):
    
    def __call__(self, x):
        return super(NeatSigmoid, self).__call__(4.9 * x)


ACTIVATION = NeatSigmoid()

MIN_BIAS = -0.1
MAX_BIAS = 0.1

WEIGHT_MUTATION_PROBABILITY = 0.8
PERTURBING_PROBABILITY = 0.9
PERTURBING_MIN = -0.2
PERTURBING_MAX = 0.2

ADD_CONNECTION_PROBABILITY = 0.05
MIN_WEIGHT = -1.0
MAX_WEIGHT = 1.0

ADD_NODE_PROBABILITY = 0.03
NEW_WEIGHT = 1.0

CROSSOVER_PROBABILITY = 0.75
DISABLE_CONNECTION_PROBABILITY = 0.75

POPULATION_SIZE = 150
MAX_GENERATIONS = 1000
SAVE_BEST_COUNT = 1

C1 = 1.0
C2 = 1.0
C3 = 0.4
N = 1
DT = 3.0


class DefaultNeat(GeneticAlgorithm):

    def __init__(self,
                 input_dim,
                 output_dim,
                 fitness_calculator):
        super().__init__(
            fitness_calculator=fitness_calculator,
            generator=UniformGenerator(input_dim, output_dim, ACTIVATION, MIN_BIAS, MAX_BIAS),
            mutations=[
                (UniformWeightMutation(PERTURBING_PROBABILITY, PERTURBING_MIN, PERTURBING_MAX, MIN_WEIGHT, MAX_WEIGHT), WEIGHT_MUTATION_PROBABILITY),
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
