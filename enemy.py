import pygame
import settings
from pygame.sprite import Sprite
class Enemy(Sprite):
    def __init__(self, fd_game):
        super().__init__()
        self.hp = fd_game.hp
        self.screen = fd_game.screen
        self.settings = fd_game.settings
        self.image = pygame.image.load('plane.bmp')
        self.rect = self.image.get_rect()
        self.shots = fd_game.shots
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def collidewithShot(self):
        if pygame.sprite.spritecollideany(self, self.shots):
            return True


    def update(self):
        self.y = self.rect.y
        self.y += (self.settings.moving_speed_y * self.settings.fleet_direction)
        self.rect.y = float(self.y)

    def get_damage(self):
        self.image = pygame.image.load('damaged_plane.bmp')

    def check_edges(self):
        # returns True, if an enemy is on the edge
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True