import pickle

from agent import Agent
from game import *
from neat.default_neat import DefaultNeat
from neat.png_exporter import PngExporter


def calculate_fitness(genomes, generation, draw_all_genomes=False):

    game = Game(
        dinos=[TRex() for _ in range(len(genomes))],
        agents=[Agent(genome) for genome in genomes],
        learning_mode=False,
        generation=generation
    )

    while game.iter(): pass

    if draw_all_genomes:
        gen_dir = f'results/gen-{generation}'
        os.mkdir(gen_dir)
        for i, ag in enumerate(sorted(game.agents, key=lambda x: x.score)):
            exporter.save(ag.genome, f'{gen_dir}/{i+1}-{ag.score}.png')

    fitness = []
    for ag in game.agents:
        fitness.append(ag.score)
    return fitness


if __name__ == '__main__':
    exporter = PngExporter()

    # TODO
    # Currently we are using 'DefaultNeat' which is actually working extremely well,
    # but I believe that there is room from progress. We should try to tweak the
    # parameters of the NEAT genetic algorithm.

    neat = DefaultNeat(4, 3, calculate_fitness, evolution_path='results/evolution')
    best_genome = neat.optimize()

    with open('best_genome.pickle', 'wb') as f:
        pickle.dump(best_genome, f, protocol=pickle.HIGHEST_PROTOCOL)
