import pygame
from src.constants import *

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, hp=100):
        super(HealthBar, self).__init__()
        # Grab the image for this platform

        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.max_hp = hp
        self.hp = hp
        self.last_hp = hp
        self.image = self.get_health_image(0, 0, 200, 30)
        self._level = 255
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



    def update_hp(self, hp):
        self.hp = hp

    def update(self, *args):
        super(HealthBar, self).update(args)
        if not self.last_hp == self.hp:
            self.image = self.get_health_image(self.rect.x, self.rect.y, self.rect.size[0], self.rect.size[1])
            self.last_hp = self.hp

    def get_health_image(self, x, y, width, height):
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        hp_width = int(max(min(self.hp / float(self.max_hp) * width, width), 0))
        pygame.draw.rect(image, RED, (0, 0, hp_width, height), 0)

        pygame.draw.rect(image, BLACK, (0, 0, width-1, height-1), 2)
        line_surface = self.font.render("HP", 0, YELLOW)
        line_width, line_height = line_surface.get_size()
        image.blit(line_surface, (5, (height // 2) - (line_height // 2) + 2))

        # # Copy the sprite from the large sheet onto the smaller image
        # image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        # image.set_colorkey(constants.BLACK)

        # Return the image
        return image