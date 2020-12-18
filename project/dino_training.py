from game import *
from neat.default_neat import DefaultNeat
from neat.png_exporter import PngExporter


class Agent:
    ACTIONS = [
        (False, False, True),  # duck
        (False, True, False),  # run
        (True, False, False)  # jump
    ]

    def __init__(self, genome):
        self.score = 0
        self.live = True
        self.genome = genome
        self.nn = genome.build_network()

    def get_next_move(self, game_speed, dino_state, obstacles_state):
        '''
        game_speed :: int -> [14, inf>
        dino_state :: boolean -> (trex_duck, trex_run, trex_jump)
        obstacles_state:: int -> list of (x, y, width, height) foreach dino
        '''

        # TODO
        # I believe that game_state is not expressive enough. Currently, neural network
        # receives [x, y, width, height] of the CLOSEST obstacle or [0, 0, 0, 0] if there is
        # no obstacle on the path + (appended) speed of the game. From my point of view,
        # we should add more information, maybe angles of some kind, or something more
        # sophisticated?

        game_state = [0, 0, 0, 0] if len(obstacles_state) == 0 else list(obstacles_state[0])
        game_state.append(game_speed)
        values = self.nn(game_state)

        max_pos = None
        max_value = None
        for i in range(len(self.ACTIONS)):
            if max_pos is None or max_value > values[i]:
                max_pos = i
                max_value = values[i]
        return self.ACTIONS[max_pos]


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

    neat = DefaultNeat(5, 3, calculate_fitness, evolution_path='results/evolution')
    best_genome = neat.optimize()

    # TODO
    # serialize best_genome so that we can exploit it later.
