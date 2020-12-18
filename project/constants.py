import pygame
import os

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

UPDATE_GAME_SPEED_THRESHOLD = 100
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
JUMPING_IMG = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
RUNNING_IMG = {
    'FIRST': pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
    'SECOND': pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))
}
DUCKING_IMG = {
    'FIRST': pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
    'SECOND': pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))
}

SMALL_CACTUS_IMG = [
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))
]

LARGE_CACTUS_IMG = [
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))
]

BIRD = [
    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))
]
