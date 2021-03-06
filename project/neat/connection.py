class Connection:

    def __init__(self, innovation, in_node_id, out_node_id, enabled, iteration, weight):
        self.innovation = innovation
        self.in_node_id = in_node_id
        self.out_node_id = out_node_id
        self.enabled = enabled
        self.iteration = iteration
        self.weight = weight

    def enable(self):
        assert not self.enabled, "Connection is already enabled."
        self.enabled = True
        self.iteration += 1

    def disable(self):
        assert self.enabled, "Connection is already disabled."
        self.enabled = False

    def copy(self):
        return Connection(self.innovation, self.in_node_id, self.out_node_id, self.enabled, self.iteration, self.weight)

    def __str__(self):
        return f"Connection(innovation = {self.innovation}, in = {self.in_node_id}, out = {self.out_node_id}, " \
               f"enabled = {self.enabled}, iteration = {self.iteration}, weight = {self.weight})"
