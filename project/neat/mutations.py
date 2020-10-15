import random

from neat.node import Node
from neat.connection import Connection


class AbstractMutation:

    def mutate(self, genome, gene_tracker):
        raise NotImplemented("Called abstract method.")


class UniformWeightMutation(AbstractMutation):

    def __init__(self, perturbing_probability, p_min, p_max, n_min, n_max):
        assert 0 <= perturbing_probability <= 1, f"Given value is not a probability: {perturbing_probability}."
        assert p_min < p_max, f"Min perturbing value must be smaller than max. Was: min={p_min}, max={p_max}."
        assert n_min < n_max, f"Min new value must be smaller than max. Was: min={n_min}, max={n_max}."
        self.perturbing_probability = perturbing_probability
        self.p_min = p_min
        self.p_max = p_max
        self.n_min = n_min
        self.n_max = n_max

    def _new_noise(self):
        random.uniform(self.p_min, self.p_max)

    def _new_weight(self):
        return random.uniform(self.n_min, self.n_max)

    def mutate(self, genome, gene_tracker):
        for connection in genome.connections:
            p = random.random()
            if p < self.perturbing_probability:
                connection.weight += self._new_noise()
            else:
                connection.weight = self._new_weight()


class AddConnectionMutation(AbstractMutation):

    def __init__(self, w_min, w_max):
        assert w_min < w_max, f"Min weight value must be smaller than max value. Was: w_min={w_min}, w_max={w_max}."
        self.w_min = w_min
        self.w_max = w_max

    def _new_weight(self):
        return random.uniform(self.w_min, self.w_max)

    def _contains_enabled_connection(self, genome, in_node_id, out_node_id):
        if not genome.contains_connection(in_node_id, out_node_id):
            return False
        return genome.get_connection(in_node_id, out_node_id).enabled

    def mutate(self, genome, gene_tracker):
        # TODO: Find a way how to efficiently determine a non-existing (or disabled) connection.
        while True:
            in_node, out_node = tuple(random.sample(genome.nodes, 2))
            if in_node.layer != out_node.layer and not self._contains_enabled_connection(genome, in_node.id, out_node.id):
                break

        if in_node.layer > out_node.layer:
            in_node, out_node = out_node, in_node

        if genome.contains_connection(in_node.id, out_node.id):
            connection = genome.get_connection(in_node.id, out_node.id)
            connection.enabled = True
            connection.iteration += 1
        else:
            innovation = gene_tracker.get_connection_innovation(in_node.id, out_node.id)
            connection = Connection(innovation, in_node.id, out_node.id, True, 0, self._new_weight())
            genome.add_connection(connection)


class AddNodeMutation(AbstractMutation):

    def __init__(self, activation, b_min, b_max, new_weight):
        assert b_min < b_max, f"Min bias value must be smaller than max value. Was: b_min={b_min}, b_max={b_max}."
        self.activation = activation
        self.b_min = b_min
        self.b_max = b_max
        self.new_weight = new_weight

    def _new_bias(self):
        return random.uniform(self.b_min, self.b_max)

    def mutate(self, genome, gene_tracker):
        possible_connections = [connection for connection in genome.connections if connection.enabled]
        count = len(possible_connections)
        if count == 0:
            return

        connection = random.choice(possible_connections)
        new_node_id = gene_tracker.get_node_id(connection.in_node_id, connection.out_node_id, connection.iteration)

        in_node_layer = genome.get_node(connection.in_node_id)
        out_node_layer = genome.get_node(connection.out_node_id)
        new_node_layer = out_node_layer
        if in_node_layer + 1 == out_node_layer:
            for node in genome.nodes:
                if node.layer == new_node_layer:
                    node.layer += 1
        genome.add_node(Node(new_node_id, new_node_layer, self.activation, self._new_bias()))

        connection.enabled = False

        innovation_in = gene_tracker.get_connection_innovation(connection.in_node_id, new_node_id)
        genome.add_connection(Connection(innovation_in, connection.in_node_id, new_node_id, True, 0, self.new_weight))

        innovation_out = gene_tracker.get_connection_innovation(new_node_id, connection.out_node_id)
        genome.add_connection(Connection(innovation_out, new_node_id, connection.out_node_id, True, 0, connection.weight))
