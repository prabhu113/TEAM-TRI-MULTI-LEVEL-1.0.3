from src import utils
import pygame

class Coin(pygame.sprite.Sprite):

    def __init__(self, image, width, height):
        super().__init__()
        self.image = pygame.surface([width, height])

        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height