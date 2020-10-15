class Node:

    def __init__(self, id, layer, activation, bias):
        self.id = id
        self.layer = layer
        self.activation = activation
        self.bias = bias

    def copy(self):
        return Node(self.id, self.layer, self.activation, self.bias)
