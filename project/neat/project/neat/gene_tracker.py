class GeneTracker:

    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self._nodes_history = {}
        self._connection_history = {}

    def get_node_id(self, in_node_id, out_node_id, iteration):
        key = in_node_id, out_node_id, iteration
        if key not in self._nodes_history:
            self._nodes_history[key] = len(self._nodes_history) + self.input_dim + self.output_dim
        return self._nodes_history[key]

    def get_connection_innovation(self, in_node_id, out_node_id):
        key = in_node_id, out_node_id
        if key not in self._connection_history:
            self._connection_history[key] = len(self._connection_history) + 1
        return self._connection_history[key]
