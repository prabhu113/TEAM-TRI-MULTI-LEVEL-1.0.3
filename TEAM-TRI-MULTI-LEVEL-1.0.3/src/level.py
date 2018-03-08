from src.screen import Screen
from src.playable import Playable
import src.constants
import pygame
from src.block import *
from src.simple_bullet import SimpleBullet
import utils
from pytmx.util_pygame import load_pygame
from random import randint
from src.health_bar import HealthBar
from src.money import Money
from src.level_manager import LevelManager

class Level(Screen, Playable):
    def __init__(self):

        self.player = None

        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000
        self.world_offset_y = 0

        # self.sprite_list = pygame.sprite.LayeredUpdates()

        self.sprite_list = pygame.sprite.LayeredUpdates()
        self.background_list = pygame.sprite.Group()

        # Solid objects
        self.solid_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.blood_list = pygame.sprite.Group()

        self.exit_list = pygame.sprite.Group()
        self.collectible_list = pygame.sprite.Group()

        self.blood_num = 0

        self.health_bar = HealthBar(20, 20, 100)
        self.sprite_list.add(self.health_bar)

        self.money = Money(0, 0)
        self.sprite_list.add(self.money)

        super(Level, self).__init__()


    def add_exit(self, sprite):
        self.sprite_list.add(sprite)
        self.exit_list.add(sprite)

    def add_collectible(self, sprite):
        self.sprite_list.add(sprite)
        self.collectible_list.add(sprite)

    def add_bullet(self, sprite):
        self.sprite_list.add(sprite)
        self.bullet_list.add(sprite)

    def add_blood(self, sprite):
        self.sprite_list.add(sprite)
        self.blood_list.add(sprite)
        self.blood_num += 1

    def add_background_sprite(self, sprite):
        self.sprite_list.add(sprite)
        self.background_list.add(sprite)

    def add_solid_sprite(self, sprite):
        """

        :param sprite:
        :return:
        """
        self.sprite_list.add(sprite)
        self.solid_list.add(sprite)

    def add_enemy(self, sprite):
        """
        Adds an enemy
        :param sprite:
        :return:
        """
        sprite._layer = 255
        self.enemy_list.add(sprite)
        self.sprite_list.add(sprite)

    def set_player(self, player):
        self.player = player
        if player not in self.sprite_list:
            player._layer = 255
            self.sprite_list.add(player)

    def handle_keyboard_event(self, event):
        player = self.player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_SPACE:
                player.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()
            if event.key == pygame.K_SPACE and player.is_shooting():
                player.stop_shooting()

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        for background_tile in self.background_list:
            # print(background_tile._layer)
            shift = 0
            if isinstance(background_tile, ParalaxBlock):
                background_tile.rect.x += shift_x // background_tile.paralax
            else:
                background_tile.rect.x += shift_x

        # Go through all the sprite lists and shift
        for platform in self.solid_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for bullet in self.bullet_list:
            bullet.rect.x += shift_x

        for blood in self.blood_list:
            blood.rect.x += shift_x

        for exit in self.exit_list:
            exit.rect.x += shift_x

        for collectible in self.collectible_list:
            collectible.rect.x += shift_x


        # self.health_bar.rect.x += shift_x

    def proceed_to_next_level(self):
        pass

    def update(self):

        super(Level, self).update()



        player = self.player
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            self.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            self.shift_world(diff)

        self.sprite_list.update()

        for bullet in self.bullet_list:
            if not bullet.dangerous:
                self.sprite_list.remove(bullet)
                self.bullet_list.remove(bullet)



        # If the player gets to the end of the level, go to the next level
        # current_position = player.rect.x + self.world_shift
        #if current_position < self.level_limit:
            # print("LIMIT")
            # player.rect.x = 120
            # if current_level_no < len(level_list) - 1:
            #     current_level_no += 1
            #     current_level = level_list[current_level_no]
            #     player.level = current_level



    def draw(self, screen):
        super(Level, self).draw(screen)
        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        # screen.fill(src.constants.BLUE)
        if self.background is not None:
            screen.blit(self.background, (self.world_shift // 3, 0))

        self.sprite_list.draw(screen)

