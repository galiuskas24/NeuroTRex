import random
from game import *


class Agent:
    ACTIONS = [
        (False, False, True),  # duck
        (False, True, False),  # run
        (True, False, False)  # jump
    ]

    def __init__(self):
        self.score = 0
        self.live = True
        self.NEAT = None

    def get_next_move(self, game_speed, dino_state, obstacles_state):
        '''
        game_speed :: int -> [14, inf>
        dino_state :: boolean -> (trex_duck, trex_run, trex_jump)
        obstacles_state:: int -> list of (x, y, width, height) foreach dino
        '''

        # TODO: NEAT prediction (now is only random choice)
        # return self.NEAT.prediction(dino_state, obstacle_state)

        next_move = random.choice(self.ACTIONS)
        return next_move

    def save_agent(self):
        # TODO: Save agent NEAT data (serialization)
        pass


if __name__ == '__main__':

    max_generations, generation = 40, 0
    num_of_dinos = 150

    while generation < max_generations:
        generation += 1

        game = Game(
            dinos=[TRex() for i in range(num_of_dinos)],
            agents=[Agent() for i in range(num_of_dinos)],
            learning_mode=False,
            generation=generation
        )

        # running game
        while game.iter(): pass

        # print stats after game
        print(f'Generation: {generation}')
        for ag in sorted(game.agents, key=lambda x: x.score):
            print(ag.score)