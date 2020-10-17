import random

from neat.gene_tracker import GeneTracker
from neat.species import Species


class GeneticAlgorithm:

    def __init__(self,
                 fitness_calculator,
                 generator,
                 mutations,
                 crossover,
                 population_size,
                 max_generations,
                 save_best_count,
                 c1, c2, c3, n, dt):
        self.fitness_calculator = fitness_calculator
        self.generator = generator
        self.mutations = mutations
        self.crossover = crossover
        self.population_size = population_size
        self.max_generations = max_generations
        self.save_best_count = save_best_count
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.n = n
        self.dt = dt

    def _generate_population(self):
        population = []
        for i in range(self.population_size):
            population.append(self.generator.generate())
        return population

    def _calculate_fitness(self, current_population):
        fitness = []
        for genome in current_population:
            fitness.append(self.fitness_calculator(build_network(genome)))
        return fitness

    def _determine_species(self, current_population, fitness, all_species):
        new_all_species = []
        for i in range(len(current_population)):
            genome = current_population[i]
            genome_fitness = fitness[i]

            for species in all_species:
                if calculate_genomes_distance(genome, species.representative, self.c1, self.c2, self.c3, self.n) < self.dt:
                    species.add_genome(genome, genome_fitness)
                    break
            else:
                new_species = Species()
                new_species.add_genome(genome, genome_fitness)
                new_all_species.append(new_species)

        all_species = [species for species in all_species if species.count != 0]
        all_species.extend(new_all_species)
        [species.finalize() for species in all_species]
        return all_species

    def _save_best(self, best_fitness, best_genome, all_species, next_population):
        for species in all_species:
            genome = species.get_genome(0)
            fitness = species.get_fitness(0)
            if best_fitness is None or fitness > best_fitness:
                best_fitness = fitness
                best_genome = genome

            save_best_count = min(self.save_best_count, species.count)
            for i in range(save_best_count):
                next_population.append(species.get_genome(i))

        return best_fitness, best_genome

    def _fill_population(self, gene_tracker, all_species, species_fitness, next_population):
        while len(next_population) < self.population_size:
            chosen_species = roulette_wheel(all_species, species_fitness)
            if chosen_species.count != 1:
                first, second = tuple(random.sample([i for i in range(chosen_species.count)], 2))
            else:
                first = second = 0
            if first > second:
                first, second = second, first

            genome1 = chosen_species.get_genome(first)
            genome2 = chosen_species.get_genome(second)
            child = genome1

            crossover, probability = self.crossover
            if random.random() < probability:
                child = crossover.cross(genome1, genome2, gene_tracker)

            for mutation, probability in self.mutations:
                if random.random() < probability:
                    mutation.mutate(child, gene_tracker)

            next_population.append(child)

    def optimize(self):
        current_population = self._generate_population()
        gene_tracker = GeneTracker(current_population[0].nodes_count)
        all_species = [Species(current_population[0])]

        best_fitness = None
        best_genome = None

        current_generation = 0
        while current_generation < self.max_generations:
            fitness = self._calculate_fitness(current_population)
            all_species = self._determine_species(current_population, fitness, all_species)
            species_fitness = [species.fitness for species in all_species]

            next_population = []
            best_fitness, best_genome = self._save_best(best_fitness, best_genome, all_species, next_population)
            self._fill_population(gene_tracker, all_species, species_fitness, next_population)
            [species.clear() for species in all_species]

            current_population = next_population
            current_generation += 1
            print(f"generation {current_generation}, best fitness: {best_fitness}")

        return build_network(best_genome)


def roulette_wheel(units, fitness):
    units_len = len(units)
    fitness_len = len(fitness)
    assert units_len != 0, "Units cannot be empty."
    assert units_len == fitness_len, f"Units and fitness must have same length. Were: {units_len} != {fitness_len}."

    position = sum(fitness) * random.random()
    current_sum = 0

    for i in range(units_len):
        current_sum += fitness[i]
        if position < current_sum:
            return units[i]
    return units[units_len-1]


def build_network(genome):
    layers = {}
    in_nodes = {}

    for node in genome.nodes:
        if node.layer not in layers:
            layers[node.layer] = []
        layers[node.layer].append(node)
        in_nodes[node.id] = []

    for connection in genome.connections:
        if connection.enabled:
            in_nodes[connection.out_node_id].append(connection.in_node_id)

    first_layer = 0
    last_layer = len(layers)-1
    input_nodes_count = len(layers[0])
    output_nodes_count = len(layers[len(layers)-1])

    def network_function(network_inputs):
        node_results = {}

        for input_node in layers[first_layer]:
            node_results[input_node.id] = network_inputs[input_node.id-1]

        for layer in range(1, last_layer+1):
            for out_node in layers[layer]:
                node_sum = 0
                for in_node in in_nodes[out_node.id]:
                    node_sum += node_results[in_node] * genome.get_connection(in_node, out_node.id).weight
                node_results[out_node.id] = out_node.activation(node_sum + out_node.bias)

        network_outputs = [0 for _ in range(output_nodes_count)]
        for output_node in layers[last_layer]:
            index = output_node.id - input_nodes_count - 1
            network_outputs[index] = node_results[output_node.id]
        return network_outputs

    return network_function


def calculate_genomes_distance(genome1, genome2, c1, c2, c3, n):
    innovation_list1 = [c.innovation for c in genome1.connections]
    innovation_list2 = [c.innovation for c in genome2.connections]
    max_innovation1 = max(innovation_list1) if len(innovation_list1) != 0 else 0
    max_innovation2 = max(innovation_list2) if len(innovation_list2) != 0 else 0
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

    excess_difference = excess_count * c1 / n
    disjoint_difference = disjoint_count * c2 / n
    weight_difference = weight_difference_sum / matching_count * c3 if matching_count != 0 else 0
    return excess_difference + disjoint_difference + weight_difference
