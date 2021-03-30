import pygame.ftfont

class Info:
    def __init__(self, fd_game):
        self.screen = fd_game.screen
        self.screen_rect = self.screen.get_rect()

        # sets info size and text
        self.width, self.height = 1280, 1024
        self.backgr_colour = (119, 136, 153)
        self.text_colour = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 50)

        # building rect and setting its position
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self._prep_txt()

    def _prep_txt(self):
        # transforms text into a rect and sets its center
        text = open('info.txt', 'r')
        posy = self.rect.top + 20
        self.screen.fill(self.backgr_colour, self.rect)
        for x in text.readlines():
            self.txt_image = self.font.render(x.rstrip(), True, self.text_colour,
                                          self.backgr_colour)
            self.txt_image_rect = self.txt_image.get_rect()
            self.txt_image_rect.centerx = self.screen_rect.centerx
            self.txt_image_rect.centery = posy

            self.screen.blit(self.txt_image, self.txt_image_rect)
            posy += 35
        text.close()

