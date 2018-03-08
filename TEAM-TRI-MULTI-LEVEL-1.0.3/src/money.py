import pygame
from src.constants import *

class Money(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Money, self).__init__()
        # Grab the image for this platform
        self.value = 0
        self.x = x
        self.y = y

        self.font = pygame.font.SysFont('Calibri', 25, True, False)

        self.image = self.get_money_image(0, SCREEN_WIDTH)

        self._level = 255
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = 10
        self.last_value = 0

        self.rect.x = self.x

    def add_money(self, value):
        self.value += value
        self.update_value(self.value)

    def update_value(self, value):
        self.value = value
        self.rect.x = self.x

    def update(self, *args):
        super(Money, self).update(args)
        if not self.last_value == self.value:
            self.image = self.get_money_image(self.rect.x, self.rect.y)
            self.last_value = self.value

    def get_money_image(self, x, y):
        line_surface = self.font.render(str(self.value), 0, YELLOW)
        line_width, line_height = line_surface.get_size()
        image = pygame.Surface([line_width, line_height], pygame.SRCALPHA).convert_alpha()
        self.x = SCREEN_WIDTH - line_width - 10

        image.blit(line_surface, (0, 0))

        return image