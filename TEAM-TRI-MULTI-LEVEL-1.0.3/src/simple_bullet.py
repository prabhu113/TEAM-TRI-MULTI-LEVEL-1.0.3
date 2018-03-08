import pygame
from src.constants import *
from src.blood_particle import BloodParticle

class SimpleBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, level):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.initial_x = x
        self.initial_y = y

        # -- Attributes
        # Set speed vector of bullet
        self.change_x = 20
        self.change_y = 0

        # What direction is the player facing?
        self.direction = direction

        self.image = pygame.Surface([4, 4])
        self.image.fill(RED)

        self.x_direction_multiplier = 1
        self.y_direction_multiplier = 1

        self.rect = self.image.get_rect()
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self._layer = 255
        self.alpha = 255
        self.dangerous = True
        self.fading = False
        self.level = level




    def stop(self):
        self.change_x = 0
        self.change_y = 0
        self.dangerous = False


    def die(self):
        self.fading = True

    def update(self):
        """ Move the bullet. """

        if self.direction == "R":
            self.x_direction_multiplier = 1
        else:
            self.x_direction_multiplier = -1

        self.rect.x += self.change_x * self.x_direction_multiplier
        self.rect.y += self.change_y * self.y_direction_multiplier

        distance_to_edge = SCREEN_WIDTH - self.initial_x
        when_to_fade = distance_to_edge * .80
        if abs(self.rect.x - self.initial_x) > when_to_fade and self.alpha >= 20:
            self.image.set_alpha(self.alpha)
            self.alpha -= 50

        if self.alpha <= 20:
            self.dangerous = False

        if self.dangerous:
            if pygame.sprite.collide_rect(self, self.level.player):
                self.level.player.take_damage(1)

            enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
            for enemy in enemy_hit_list:

                enemy.take_damage(1)
                self.stop()

                for i in range(100):
                    bloodParticle = BloodParticle(self.rect.x, self.rect.y, self.direction, self.level)
                    self.level.add_blood(bloodParticle)
                break





