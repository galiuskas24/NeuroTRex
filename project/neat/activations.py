from math import exp, tanh


class AbstractActivation:

    def __call__(self, x):
        raise NotImplemented("Called abstract method.")

    def __str__(self):
        return type(self).__name__


class Identity(AbstractActivation):

    def __call__(self, x):
        return x


class Sigmoid(AbstractActivation):

    def __call__(self, x):
        return 1.0 / (1 + exp(-x))


class Tanh(AbstractActivation):

    def __call__(self, x):
        return tanh(x)


class ReLU(AbstractActivation):

    def __call__(self, x):
        return max(0, x)
