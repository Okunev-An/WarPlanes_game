import pygame

class Stats:
    def __init__(self, fd_game):
        self.settings = fd_game.settings
        self.reset_stats()
        self.game_active = False
        self.game_paused = False
        self.info_open = False
        # get high score from txt file
        hs = open('record.txt', 'r')
        self.high_score = int(hs.read().strip())
    def reset_stats(self):
        self.lives_left = self.settings.tries_limit

        self.level = 1
        self.score = 0

    