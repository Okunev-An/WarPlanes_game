import pygame
from pygame.sprite import Sprite

class Junkers(Sprite):

    def __init__(self, fd_game):
        super().__init__()
        self.screen = fd_game.screen
        self.screen_rect = fd_game.screen.get_rect()
        self.settings = fd_game.settings

        self.image = pygame.image.load('junkers.bmp')
        self.rect = self.image.get_rect()
        self.center_plane()
        self.x = self.rect.x
        self.y = self.rect.y
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.junkers_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.junkers_speed
        if self.moving_up and self.rect.y > self.screen_rect.y:
            self.y -= self.settings.junkers_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.junkers_speed
        self.rect.x, self.rect.y = self.x, self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_plane(self):
        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.right - 20
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)