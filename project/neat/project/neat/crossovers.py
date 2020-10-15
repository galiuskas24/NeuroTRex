import random

from neat.genome import Genome


class AbstractCrossover:

    """
    Bear in mind that genome1 must have better fitness than genome2.
    It is callers responsibility to assure that.
    """
    def cross(self, genome1, genome2, gene_tracker):
        raise NotImplemented("Called abstract method.")


class ComposedCrossover(AbstractCrossover):

    def __init__(self, crossovers, portions):
        crossovers_len = len(crossovers)
        portions_len = len(portions)
        assert crossovers_len != 0, "Crossover list cannot be empty."
        assert crossovers_len != portions_len, f"Crossover list and portion list must have same length. Were: {crossovers_len} != {portions_len}."

        self.crossovers = crossovers

        self.portion_sum = 0
        for portion in portions:
            assert portions > 0, f"Portion must be positive. Was: {portion}."
            self.portion_sum += portions

        self.positions = []
        for i in range(portions_len):
            self.positions[i] = (0 if i == 0 else self.positions[i-1]) + portions[i]

    def cross(self, genome1, genome2, gene_tracker):
        position = random.random() * self.portion_sum
        count = len(self.crossovers)

        for i in range(count):
            if position < self.positions[i]:
                self.crossovers[i].cross(genome1, genome2)
                break
        else:
            self.crossovers[count-1].cross(genome1, genome2)


class StandardCrossover(AbstractCrossover):

    def __init__(self, disable_probability):
        self.disable_probability = disable_probability

    def cross(self, genome1, genome2, gene_tracker):
        child_genome = Genome()
        for node in genome1.nodes:
            child_genome.add_node(node.copy())

        for connection in genome1.connection:
            new_connection = connection.copy()
            if genome2.contains_connection(new_connection.in_node_id, new_connection.out_node_id):
                other_connection = genome2.get_connection(new_connection.in_node_id, new_connection.out_node_id)
                if not new_connection.enabled or not other_connection.enabled:
                    new_connection.enabled = random.random() < self.disable_probability
                if random.choice([True, False]):
                    new_connection.weight = other_connection.weight
            child_genome.add_connection(new_connection)

        return child_genome
