from constants import *
import random


class TRex:
    X, Y = 80, 318
    Y_DUCK = 340
    CYCLE_LEN = 10
    JUMP_VELOCITY = 34

    def __init__(self):
        self.trex_run = True
        self.trex_jump = False
        self.trex_duck = False
        self.live = True

        self.img_of_run = RUNNING_IMG
        self.img_of_jump = JUMPING_IMG
        self.img_of_duck = DUCKING_IMG

        self.step = 0
        self.jump_vel = self.JUMP_VELOCITY
        self.image = self.img_of_run['FIRST']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.X, self.Y

    def run(self):
        self.image = self.img_of_run['FIRST'] if self.step < (self.CYCLE_LEN / 2) else self.img_of_run['SECOND']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.X, self.Y
        self.step += 1

    def jump(self):
        self.image = self.img_of_jump

        if self.jump_vel < -self.JUMP_VELOCITY:
            self.trex_jump = False
            self.jump_vel = self.JUMP_VELOCITY
            self.rect.y = self.Y

        if self.trex_jump:
            self.rect.y -= self.jump_vel
            self.jump_vel -= 3.2

    def duck(self):
        self.image = self.img_of_duck['FIRST'] if self.step < (self.CYCLE_LEN / 2) else self.img_of_duck['SECOND']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.X, self.Y_DUCK
        self.step += 1

    def get_state(self):
        return self.trex_duck, self.trex_run, self.trex_jump

    def update_with_agent(self, next_move):
        # call function for action
        if self.trex_jump: self.jump()
        if self.trex_duck: self.duck()
        if self.trex_run: self.run()

        # update counter
        self.step %= self.CYCLE_LEN

        # action
        down, run, up = next_move

        # do action with checking
        if up and not self.trex_jump:
            self.trex_run, self.trex_duck, self.trex_jump = False, False, True
        elif down and not self.trex_jump:
            self.trex_run, self.trex_duck, self.trex_jump = False, True, False
        elif not self.trex_jump and not down:
            self.trex_run, self.trex_duck, self.trex_jump = True, False, False

    def update(self, user_input):
        # call function for action
        if self.trex_jump: self.jump()
        if self.trex_duck: self.duck()
        if self.trex_run: self.run()

        # update counter
        self.step %= self.CYCLE_LEN

        # actions
        if user_input[pygame.K_UP] and not self.trex_jump:
            self.trex_run, self.trex_duck, self.trex_jump = False, False, True
        elif user_input[pygame.K_DOWN] and not self.trex_jump:
            self.trex_run, self.trex_duck, self.trex_jump = False, True, False
        elif not self.trex_jump and not user_input[pygame.K_DOWN]:
            self.trex_run, self.trex_duck, self.trex_jump = True, False, False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Background:
    X, Y = 0, 380

    def __init__(self):
        self.screen_width = SCREEN_WIDTH

        # floor
        self.floor_img = BG
        self.floor_img_width = self.floor_img.get_width()
        self.fl_x, self.fl_y = self.X, self.Y

        # cloud
        self.cloud_img = CLOUD
        self.cloud_img_width = self.cloud_img.get_width()
        self.cl_x = self.screen_width + random.randint(800, 1000)
        self.cl_y = random.randint(50, 100)


    def update(self, game_speed):
        # floor
        self.fl_x -= game_speed

        # cloud
        self.cl_x -= game_speed

        if self.cl_x <= -self.cloud_img_width:
            self.cl_x = self.screen_width + random.randint(2500, 3000)
            self.cl_y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.floor_img, (self.fl_x, self.fl_y))
        screen.blit(self.floor_img, (self.fl_x + self.floor_img_width, self.fl_y))
        screen.blit(self.cloud_img, (self.cl_x, self.cl_y))

        if self.fl_x <= -self.floor_img_width:
            screen.blit(self.floor_img, (self.fl_x + self.floor_img_width, self.fl_y))
            self.fl_x = 0


class Obstacle:

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

    @staticmethod
    def get_state(obstacles):
        return [(obs.rect.x, obs.rect.y, obs.rect.width, obs.rect.height) for obs in obstacles]


class SmallCactus(Obstacle):

    def __init__(self):
        self.image = SMALL_CACTUS_IMG
        self.type = random.randint(0, 2)
        super().__init__(self.image, self.type)
        self.rect.y = 325


class BigCactus(Obstacle):

    def __init__(self):
        self.image = LARGE_CACTUS_IMG
        self.type = random.randint(0, 2)
        super().__init__(self.image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    CYCLE_LEN = 10

    def __init__(self):
        self.type = 0
        self.image = BIRD
        super().__init__(self.image, self.type)
        self.rect.y = 265
        self.step = 0

    def draw(self, screen):
        '''
        Override method from Obstacle.
        '''
        self.step += 1
        self.step %= self.CYCLE_LEN
        image = self.image[0] if self.step < (self.CYCLE_LEN / 2) else self.image[1]
        screen.blit(image, self.rect)
