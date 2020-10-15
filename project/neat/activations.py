from math import exp, tanh


def sigmoid(x):
    return 1.0 / (1 + exp(-x))


def tanh(x):
    return tanh(x)


def relu(x):
    return max(0, x)
