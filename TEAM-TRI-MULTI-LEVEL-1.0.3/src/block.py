import src.utils
import pygame
from src import utils
from src.blood_particle import BloodParticle
from src.animated_block import AnimatedBlock
from random import randint
from src.simple_bullet import SimpleBullet

class Block(pygame.sprite.Sprite):
    """ Basic block of sprite """

    def __init__(self, image, x, y):
        super().__init__()

        # Grab the image for this platform
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class ExitBlock(Block):
    """ This block designates level switch/ an exit"""
    def __init__(self, image, x, y):
        super(ExitBlock, self).__init__(image, x, y)

class Collectible(Block):
    """ This block is a colletible and will add to a money bag"""
    def __init__(self, image, x, y, value):
        super(Collectible, self).__init__(image, x, y)
        self.value = value
        self.sound = pygame.mixer.Sound(
            utils.get_asset_path('ring_inventory.wav'))

    def kill(self):
        self.sound.play()
        super(Collectible, self).kill()



class Enemy(AnimatedBlock):
    """ Basic enemy, will cause damage """
    def __init__(self, image, x, y, hp):
        super(Enemy, self).__init__(image, x, y)
        self.max_hp = hp
        self.hp = hp
        self.alpha = 255
        self.change_in_y = 1
        self.jump_up = True
        self.impact_sound = pygame.mixer.Sound(
            utils.get_asset_path('394213__chance4doom__bullet-impact-1.ogg'))

        self.can_shoot = False
        self.can_jump = True

    def take_damage(self, damage):
        print("taking damage hp", self.hp)
        self.hp -= damage
        
        self.impact_sound.play()
        if self.hp <= 1:
            print("ENEMY DEAD!")


    def update(self, *args):
        super(Enemy, self).update(args)
        # self.jump()


        if self.can_jump:
            self.calc_grav()
            if 10 > randint(1, 1000):
                self.jump()
        else:
            self.glide()



        if self.can_shoot:
            if 10 > randint(1, 5000):
                self.stop_shooting()
            elif 10 > randint(1, 5000):
                self.shoot()


        #
        # # Move left/right
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        alpha =  self.hp * 255 / self.max_hp
        # print("setting alpha", alpha, "hp", self.hp)
        self.image.set_alpha(alpha)

        if self.hp < 1:
            self.kill()

            # # Bullets
        if self.shooting:
            bullet_x = self.rect.x + 50
            if self.direction == "L":
                bullet_x = self.rect.x - 50
            bullet = SimpleBullet(bullet_x, self.rect.y + 40, self.direction, self.level)
            bullet.change_y = 5
            self.level.add_bullet(bullet)


class ParalaxBlock(Block):
    """ These blocks will shift with backgound """
    def __init__(self, image, x, y, paralax):
        super().__init__(image, x, y)

        self.paralax = paralax
