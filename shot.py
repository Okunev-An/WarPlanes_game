import pygame
from pygame.sprite import Sprite
import random

class Shot(Sprite):
    def __init__(self, fd_game, direction=1, color=(50, 50, 50), shooter='junkers'):
        super().__init__()
        self.settings = fd_game.settings
        self.screen = fd_game.screen
        self.colour = color
        self.rect = pygame.Rect(0, 0, 10, 3)
        if shooter == 'junkers':
            self.rect.midleft = fd_game.junkers.rect.midleft
        elif shooter == 'enemy':
            self.shooting_enemy = random.choice(list(fd_game.enemies))
            self.rect.midright = self.shooting_enemy.rect.midright
        self.x = float(self.rect.x)
        self.direction = direction

    def update(self):
        self.x -= (self.direction * self.settings.shot_speed if self.direction > 0
                   else self.direction * self.settings.enemy_shot_speed)
        self.rect.x = self.x


    def draw_shot(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)


