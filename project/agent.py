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
            if max_pos is None or values[i] > max_value:
                max_pos = i
                max_value = values[i]
        return self.ACTIONS[max_pos]