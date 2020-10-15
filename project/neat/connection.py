class Connection:

    def __init__(self, innovation, in_node_id, out_node_id, enabled, iteration, weight):
        self.innovation = innovation
        self.in_node_id = in_node_id
        self.out_node_id = out_node_id
        self.enabled = enabled
        self.iteration = iteration
        self.weight = weight

    def copy(self):
        return Connection(self.innovation, self.in_node_id, self.out_node_id, self.enabled, self.iteration, self.weight)
