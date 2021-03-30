import pygame.font
class Button:
    def __init__(self, fd_game, msg, bias=(0, 0), colour=(127, 255, 0)):
        # initializes button attributes
        self.screen = fd_game.screen
        screen_rect = self.screen.get_rect()

        # sets button size and funcs
        self.width, self.height = 220, 75
        self.button_colour = colour
        self.text_colour = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 50)
        self.bias = bias

        # building button rect and setting its position
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = screen_rect.centerx + self.bias[0]
        self.rect.centery = screen_rect.centery + self.bias[1]

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # transforms msg into a rect and sets its center
        self.msg_image = self.font.render(msg, True, self.text_colour,
                                          self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # shows empty button and prints message
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)