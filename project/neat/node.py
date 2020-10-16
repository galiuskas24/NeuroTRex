class Node:

    def __init__(self, id, layer, activation, bias):
        self.id = id
        self.layer = layer
        self.activation = activation
        self.bias = bias

    def copy(self):
        return Node(self.id, self.layer, self.activation, self.bias)

    def __str__(self):
        return f"Node(id = {self.id}, layer = {self.layer}, activation = {self.activation}, bias = {self.bias})"
