import random

from neat.activations import Identity
from neat.genome import Genome
from neat.node import Node


class AbstractGenerator:

    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim

    def generate(self):
        raise NotImplemented("Called abstract method.")


class ComposedGenerator(AbstractGenerator):

    def __init__(self, input_dim, output_dim, generators, portions):
        super().__init__(input_dim, output_dim)
        generators_len = len(generators)
        portions_len = len(portions)
        assert generators_len != 0, "Generator list cannot be empty."
        assert generators_len == portions_len, f"Generator list and portion list must have same length. Were: {generators_len} != {portions_len}."

        self.generators = generators

        self.portion_sum = 0
        for portion in portions:
            assert portion > 0, f"Portion must be positive. Was: {portion}."
            self.portion_sum += portion

        self.positions = []
        for i in range(portions_len):
            self.positions.append((0 if i == 0 else self.positions[i-1]) + portions[i])

    def generate(self):
        position = random.random() * self.portion_sum
        count = len(self.generators)

        for i in range(count):
            if position < self.positions[i]:
                return self.generators[i].generate()
        else:
            return self.generators[count-1].generate()


class UniformGenerator(AbstractGenerator):

    INPUT_ACTIVATION = Identity()
    INPUT_BIAS = 0.0

    def __init__(self, input_dim, output_dim, output_activation, b_min, b_max):
        super().__init__(input_dim, output_dim)
        self.b_min = b_min
        self.b_max = b_max
        self.output_activation = output_activation

    def _new_bias(self):
        return random.uniform(self.b_min, self.b_max)

    def generate(self):
        genome = Genome()
        for i in range(self.input_dim):
            genome.add_node(Node(i+1, 0, UniformGenerator.INPUT_ACTIVATION, UniformGenerator.INPUT_BIAS))
        for i in range(self.output_dim):
            genome.add_node(Node(i+1+self.input_dim, 1, self.output_activation, self._new_bias()))
        return genome
