import random

from neat.genome import Genome


class AbstractCrossover:

    """
    Bear in mind that genome1 must have better fitness than genome2.
    It is callers responsibility to assure that.
    """
    def cross(self, genome1, genome2, gene_tracker):
        raise NotImplemented("Called abstract method.")


class StandardCrossover(AbstractCrossover):

    def cross(self, genome1, genome2, gene_tracker):
        child_genome = Genome()
        for node in genome1.nodes:
            child_genome.add_node(node.copy())

        for connection in genome1.connection:
            new_connection = connection.copy()
            if genome2.contains_connection(new_connection.in_node_id, new_connection.out_node_id):
                if random.choice([True, False]):
                    other_connection = genome2.get_connection(new_connection.in_node_id, new_connection.out_node_id)
                    new_connection.weight = other_connection.weight
            child_genome.add_connection(new_connection)

        return child_genome
