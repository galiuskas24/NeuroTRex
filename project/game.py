from utility import *


class Game:

    @staticmethod
    def play_for_fun():
        pygame.init()
        pygame.display.set_caption('Neuro T-Rex')
        GAME_IS_RUNNING = True
        clock = pygame.time.Clock()
        dino = TRex()
        background = Background()
        obstacles = []
        acceleration = 14

        while GAME_IS_RUNNING:
            # exit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAME_IS_RUNNING = False

            user_input = pygame.key.get_pressed()

            # create new frame
            SCREEN.fill(WHITE)
            dino.draw(SCREEN)
            dino.update(user_input)

            background.draw(SCREEN)
            background.update(acceleration)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus())
                elif random.randint(0, 2) == 1:
                    obstacles.append(BigCactus())
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird())

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update(acceleration, obstacles)
                if dino.rect.colliderect(obstacle.rect):
                    pygame.draw.rect(SCREEN, (255, 0, 0), dino.rect, 2)
                    # pygame.time.delay(2000)
                    # death_count += 1
                    # menu(death_count)

            clock.tick(30)
            pygame.display.update()

    def __init__(self, dinos, agents, learning_mode, generation):
        pygame.init()
        pygame.display.set_caption('Neuro T-Rex game')

        self.clock = pygame.time.Clock()
        self.background = Background()
        self.generation = generation
        self.dinos = dinos
        self.agents = agents
        self.obstacles = []
        self.learning_mode = learning_mode
        self.game_speed = 14
        self.time = 0
        self.screen = SCREEN
        self.font = pygame.font.Font('freesansbold.ttf', 25)

    def print_score(self):
        text = 'Gen: ' + str(self.generation)
        text += ' Live: ' + str(len([ag for ag in self.agents if ag.live]))
        text += ' Score: ' + str(self.time)
        text = self.font.render(text, True, BLACK)
        textRect = text.get_rect()
        textRect.center = (800, 40)
        self.screen.blit(text, textRect)

    def iter(self):
        self.time += 1

        # end game conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # ----- CREATE NEW FRAME ------
        self.screen.fill(WHITE)

        # draw dinos
        end_game = True
        for dino, agent in zip(self.dinos, self.agents):
            if dino.live and agent.live:
                end_game = False
                dino.draw(self.screen)
                next_move = agent.get_next_move(self.game_speed, dino.get_state(), Obstacle.get_state(self.obstacles))
                dino.update_with_agent(next_move)

        if end_game: return False

        # draw background
        self.background.draw(self.screen)
        self.background.update(self.game_speed)

        # draw one obstacle
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                self.obstacles.append(SmallCactus())
            elif random.randint(0, 2) == 0:
                self.obstacles.append(BigCactus())
            elif random.randint(0, 2) == 0:
                self.obstacles.append(Bird())

        # collision detector
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            obstacle.update(self.game_speed, self.obstacles)

            for dino, agent in zip(self.dinos, self.agents):
                if dino.live and agent.live:
                    if dino.rect.colliderect(obstacle.rect):
                        # pygame.draw.rect(self.screen, (255, 0, 0), dino.trex_rect, 2)
                        agent.score = self.time
                        dino.live, agent.live = False, False

        # update game_speed
        if self.time % UPDATE_GAME_SPEED_THRESHOLD == 0:
            self.game_speed += 1

        # print score and update pygame
        self.print_score()
        if not self.learning_mode: self.clock.tick(30)
        pygame.display.update()
        
        return True


if __name__ == '__main__':
    Game.play_for_fun()


