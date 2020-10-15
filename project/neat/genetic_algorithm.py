
def build_network(genome):
    layers = {}
    in_nodes = {}

    for node in genome.nodes:
        if node.layer not in layers:
            layers[node.layer] = []
        layers[node.layer].append(node)
    first_layer = 0
    last_layer = len(layers)-1
    input_nodes_count = len(layers[0])
    output_nodes_count = len(layers[len(layers)-1])

    for connection in genome.connections:
        if connection.out_node_id not in in_nodes:
            in_nodes[connection.out_node_id] = []
        in_nodes[connection.out_node_id].append(connection.in_node_id)

    def network_function(network_inputs):
        node_results = {}

        for input_node in layers[first_layer]:
            node_results[input_node.id] = network_inputs[input_node.id-1]

        for layer in range(1, last_layer+1):
            for out_node in layers[layers]:
                node_sum = 0
                for in_node in in_nodes[out_node.id]:
                    node_sum += node_results[in_node.id] * genome.get_connection(in_node.id, out_node.id).weight
                node_results[out_node.id] = out_node.activation(node_sum + out_node.bias)

        network_outputs = [0 for _ in range(output_nodes_count)]
        for output_node in layers[last_layer]:
            index = output_node.id - input_nodes_count - 1
            network_outputs[index] = node_results[output_node.id]
        return network_outputs

    return network_function


def calculate_genomes_distance(genome1, genome2, c1, c2, c3, n):
    max_innovation1 = max([c.innovation for c in genome1.connections])
    max_innovation2 = max([c.innovation for c in genome2.connections])
    split_point = min(max_innovation1, max_innovation2)

    excess_count = 0
    disjoint_count = 0
    matching_count = 0
    weight_difference_sum = 0

    for connection1 in genome1.connections:
        if genome2.contains_connection(connection1.in_node_id, connection1.out_node_id):
            connection2 = genome2.get_connection(connection1.in_node_id, connection1.out_node_id)
            matching_count += 1
            weight_difference_sum += abs(connection1.weight - connection2.weight)
        elif connection1.innovation > split_point:
            excess_count += 1
        elif connection1.innovation <= split_point:
            disjoint_count += 1

    for connection2 in genome2.connections:
        if not genome1.contains_connection(connection2.in_node_id, connection2.out_node_id):
            if connection2.innovation > split_point:
                excess_count += 1
            else:
                disjoint_count += 1

    return excess_count * c1 / n + disjoint_count * c2 / n + weight_difference_sum / matching_count * c3
