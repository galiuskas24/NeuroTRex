class Genome:

    def __init__(self):
        self.nodes_dict = {}
        self.connections_dict = {}

    def copy(self):
        genome_copy = Genome()
        for node in self.nodes:
            genome_copy.add_node(node.copy())
        for connection in self.connections:
            genome_copy.add_connection(connection.copy())
        return genome_copy

    @property
    def nodes_count(self):
        return len(self.node_ids)

    def contains_node(self, node_id):
        return node_id in self.nodes_dict

    def get_node(self, node_id):
        assert self.contains_node(node_id), f"Node with id: {node_id} does not exist."
        return self.nodes_dict[node_id]

    def add_node(self, node):
        assert not self.contains_node(node.id), f"Duplicate node id: {node.id}."
        self.nodes_dict[node.id] = node

    @property
    def node_ids(self):
        return self.nodes_dict.keys()

    @property
    def nodes(self):
        return list(self.nodes_dict.values())

    @property
    def connections_count(self):
        return len(self.connections_dict)

    def contains_connection(self, in_node_id, out_node_id):
        key = in_node_id, out_node_id
        return key in self.connections_dict

    def get_connection(self, in_node_id, out_node_id):
        assert self.contains_connection(in_node_id, out_node_id), \
               f"Connection with in_node_id={in_node_id} and out_node_id={out_node_id} does not exist."
        return self.connections_dict[(in_node_id, out_node_id)]

    def add_connection(self, connection):
        in_node_id = connection.in_node_id
        out_node_id = connection.out_node_id
        assert self.contains_node(in_node_id), f"Input node with id: {in_node_id} does not exist."
        assert self.contains_node(out_node_id), f"Output node with id: {out_node_id} does not exist."
        assert not self.contains_connection(in_node_id, out_node_id), \
               f"Connection with in_node_id={in_node_id} and out_out_id={out_node_id} already exists."
        self.connections_dict[(in_node_id, out_node_id)] = connection

    @property
    def connection_ids(self):
        return self.connections_dict.keys()

    @property
    def connections(self):
        return list(self.connections_dict.values())

    def __str__(self):
        string = "Nodes:\n"
        string += "\n".join([str(node) for node in self.nodes])
        string += "\n"
        string += "Connections:\n"
        string += "\n".join([str(connection) for connection in self.connections])
        return string

    def build_network(self):
        layers = {}
        in_nodes = {}

        for node in self.nodes:
            if node.layer not in layers:
                layers[node.layer] = []
            layers[node.layer].append(node)
            in_nodes[node.id] = []

        for connection in self.connections:
            if connection.enabled:
                in_nodes[connection.out_node_id].append(connection.in_node_id)

        first_layer = 0
        last_layer = len(layers)-1
        input_nodes_count = len(layers[0])
        output_nodes_count = len(layers[len(layers)-1])

        def network_function(network_inputs):
            node_results = {}

            for input_node in layers[first_layer]:
                node_results[input_node.id] = network_inputs[input_node.id-1]

            for layer in range(1, last_layer+1):
                for out_node in layers[layer]:
                    node_sum = 0
                    try:
                        for in_node in in_nodes[out_node.id]:
                            node_sum += node_results[in_node] * self.get_connection(in_node, out_node.id).weight
                        node_results[out_node.id] = out_node.activation(node_sum + out_node.bias)
                    except OverflowError:
                        node_results[out_node.id] = float('inf')

            network_outputs = [0 for _ in range(output_nodes_count)]
            for output_node in layers[last_layer]:
                index = output_node.id - input_nodes_count - 1
                network_outputs[index] = node_results[output_node.id]
            return network_outputs

        return network_function
