import pygame
from src.constants import *
from random import uniform, randint

class BloodParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, level):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.initial_x = x + uniform(0, 20)
        self.initial_y = y + uniform(-4, 20)

        # -- Attributes
        # Set speed vector of bullet
        self.change_x = uniform(-5, 20)
        self.change_y = uniform(-20, 10)

        # What direction is the player facing?
        self.direction = direction

        self.image = pygame.Surface([randint(1, 2), randint(2, 6)])
        self.image.fill(RED)

        self.x_direction_multiplier = 1
        self.y_direction_multiplier = 1

        self.x_velocity_multiplier = uniform(1, 20)
        self.y_velocity_multiplier = uniform(0.2, 2)


        self.rect = self.image.get_rect()
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self._layer = 255
        self.alpha = 255
        self.fading = False
        self.level = level
        self.ttl = pygame.time.get_ticks()
        self.on_ground = False


    def calc_grav(self):
        """ Calculate effect of gravity. """

        self.change_y += self.y_velocity_multiplier


        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.change_x = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.on_ground = True


    def stop(self):
        self.change_x = 0
        self.change_y = 0


    def die(self):
        self.fading = True

    def update(self):
        """ Move the bullet. """

        self.calc_grav()

        if self.direction == "R":
            self.x_direction_multiplier = 1
        else:
            self.x_direction_multiplier = -1

        self.rect.x += self.change_x * self.x_direction_multiplier
        self.rect.y += self.change_y * self.y_direction_multiplier

        distance_to_edge = SCREEN_WIDTH - self.initial_x

        # len(self.level.blood_list) > 1000
        if self.on_ground and self.level.blood_num > 200 and pygame.time.get_ticks() - self.ttl > 5000:
            self.die()

        if self.fading:
            self.image.set_alpha(self.alpha)
            self.alpha -= 50

        if self.alpha <= 20:
            self.kill()
            self.level.blood_num -= 1


        # if self.dangerous:
        if self.rect.colliderect(self.level.player):
            self.stop()






