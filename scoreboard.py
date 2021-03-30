import pygame.font
from pygame.sprite import Group
from junkers import Junkers

class Scoreboard():
    # a class to draw game info
    def __init__(self, fd_game):
        # initializes attributes of score counting
        self.fd_game = fd_game
        self.screen = fd_game.screen
        self.screen_rect = fd_game.screen.get_rect()
        self.settings = fd_game.settings
        self.stats = fd_game.stats

        # font settings to draw a score
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 36)
        # preparing scores images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # transforms current score into image
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                            self.text_color, self.settings.bg_colour)
        # prints score in the screen' top right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.left + 250
        self.score_rect.top = 20

    def prep_high_score(self):
        # transforms high score into image
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                self.text_color, self.settings.bg_colour)
        # highscore centers on the screen top
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midleft = self.screen_rect.midleft
        self.high_score_rect.right = self.score_rect.right
        self.high_score_rect.top = self.score_rect.top + 500
    def prep_level(self):
        # transforms level into image
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                           self.text_color, self.settings.bg_colour)

        # level is shown under current score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        # tells number ships left
        self.junkersen = Group()
        for junkers_number in range(self.stats.lives_left):
            junkers = Junkers(self.fd_game)
            junkers.rect.x = 10
            junkers.rect.y = self.screen_rect.top +\
                    100 + (junkers_number * junkers.rect.height)
            self.junkersen.add(junkers)


    def check_high_score(self):
        # checks if current score is new highscore
        if self.stats.score > self.stats.high_score:
            hs = open('record.txt', 'w')
            hs.write(str(self.stats.score))
            hs.close()
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        # draws score on the screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.junkersen.draw(self.screen)