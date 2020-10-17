import random


class GenomeFitness:

    def __init__(self, genome, fitness):
        self.genome = genome
        self.fitness = fitness


class Species:

    def __init__(self, representative=None):
        self.genomes = []
        self.fitness_sum = 0
        self.representative = representative
        self.finalized = False

    @property
    def count(self):
        return len(self.genomes)

    @property
    def fitness(self):
        return self.fitness_sum / self.count

    def get_genome(self, index):
        return self.genomes[index].genome

    def get_fitness(self, index):
        return self.genomes[index].fitness

    def add_genome(self, genome, fitness):
        assert not self.finalized, "Species were finalized. Cannot add new genome. Call clear before add_genome."
        self.genomes.append(GenomeFitness(genome, fitness))
        self.fitness_sum += fitness

    def finalize(self):
        self.finalized = True
        self.genomes.sort(key=lambda g: g.fitness)
        self.representative = random.choice(self.genomes).genome

    def clear(self):
        self.finalized = False
        self.genomes.clear()
        self.fitness_sum = 0
