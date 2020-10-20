from neat.activations import Identity, ReLU
from neat.connection import Connection
from neat.genome import Genome
from neat.node import Node
from png_exporter import PngExporter

genome = Genome()
genome.add_node(Node(1, 0, Identity(), 0.0))
genome.add_node(Node(2, 0, Identity(), 0.0))
genome.add_node(Node(3, 0, Identity(), 0.0))

genome.add_node(Node(6, 1, ReLU(), 1.0))
genome.add_node(Node(7, 1, ReLU(), 1.0))
genome.add_node(Node(8, 1, ReLU(), 1.0))
genome.add_node(Node(9, 1, ReLU(), 1.0))
genome.add_node(Node(10, 1, ReLU(), 1.0))

genome.add_node(Node(11, 2, ReLU(), 1.0))
genome.add_node(Node(12, 2, ReLU(), 1.0))
genome.add_node(Node(13, 2, ReLU(), 1.0))
genome.add_node(Node(14, 2, ReLU(), 1.0))

genome.add_node(Node(15, 3, ReLU(), 1.0))
genome.add_node(Node(16, 3, ReLU(), 1.0))
genome.add_node(Node(17, 3, ReLU(), 1.0))

genome.add_node(Node(4, 4, ReLU(), 1.0))
genome.add_node(Node(5, 4, ReLU(), 1.0))

genome.add_connection(Connection(1, 1, 6, True, 0, 0.5))
genome.add_connection(Connection(1, 1, 7, True, 0, -1.0))
genome.add_connection(Connection(1, 1, 9, True, 0, -0.4))

genome.add_connection(Connection(1, 2, 6, True, 0, 0.7))
genome.add_connection(Connection(1, 2, 7, True, 0, -0.1))

genome.add_connection(Connection(1, 3, 6, False, 0, 0.6))
genome.add_connection(Connection(1, 3, 9, True, 0, -0.18))
genome.add_connection(Connection(1, 3, 8, True, 0, 0.72))
genome.add_connection(Connection(1, 3, 7, True, 0, -0.9))

genome.add_connection(Connection(1, 6, 11, True, 0, 0.6))
genome.add_connection(Connection(1, 6, 13, False, 0, -0.5))
genome.add_connection(Connection(1, 7, 14, True, 0, 1.0))
genome.add_connection(Connection(1, 7, 12, True, 0, -0.9))
genome.add_connection(Connection(1, 8, 11, True, 0, 0.7))
genome.add_connection(Connection(1, 9, 13, True, 0, -0.7))
genome.add_connection(Connection(1, 9, 12, False, 0, -0.01))
genome.add_connection(Connection(1, 10, 13, False, 0, -0.7))

genome.add_connection(Connection(1, 11, 15, True, 0, -0.62))
genome.add_connection(Connection(1, 12, 15, False, 0, -0.28))
genome.add_connection(Connection(1, 13, 16, True, 0, 0.42))
genome.add_connection(Connection(1, 14, 17, True, 0, -0.95))
genome.add_connection(Connection(1, 11, 4, True, 0, -0.2))
genome.add_connection(Connection(1, 12, 5, False, 0, -0.1))
genome.add_connection(Connection(1, 14, 4, True, 0, -0.5))
genome.add_connection(Connection(1, 13, 4, True, 0, 0.32))
genome.add_connection(Connection(1, 16, 4, False, 0, -0.4))
genome.add_connection(Connection(1, 16, 5, True, 0, 0.82))

exporter = PngExporter(width=1920, height=1080, show_disabled=True)
exporter.save(genome, "test-export.png")
