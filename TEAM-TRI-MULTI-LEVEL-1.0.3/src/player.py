"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame
from src import utils
from src import constants
from src.simple_bullet import SimpleBullet
from src.level_manager import *
from src.level import Level

#from platforms import MovingPlatform
from src.spritesheet_functions import SpriteSheet


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # -- Attributes
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # This holds all the images for the animated walk left/right
        # of our player
        self.state_frames = dict()

        self.state = P_STATE_NORMAL
        self.old_state = P_STATE_NORMAL

        # What direction is the player facing?
        self.direction = "R"

        self.money = 0

        # List of sprites we can bump against
        self.level = None

        self.state_frames = { P_STATE_NORMAL: { "R": self.get_walking_frames("p1_walk.png"),
                                                "L": self.get_walking_frames("p1_walk.png", True)},
                              P_STATE_SHOOTING: { "R": self.get_walking_frames("p1_shoot.png"),
                                                  "L": self.get_walking_frames("p1_shoot.png", True)},
                              P_STATE_DAMAGE: {"R": self.get_walking_frames("p1_damage.png"),
                                                 "L": self.get_walking_frames("p1_damage.png", True)},
                              P_STATE_NORMAL_90: {"R": self.get_walking_frames("p1_walk_90.png"),
                                                 "L": self.get_walking_frames("p1_walk_90.png", True)},
                              P_STATE_NORMAL_50: {"R": self.get_walking_frames("p1_walk_50.png"),
                                                 "L": self.get_walking_frames("p1_walk_50.png", True)},
                              P_STATE_NORMAL_30: {"R": self.get_walking_frames("p1_walk_30.png"),
                                                 "L": self.get_walking_frames("p1_walk_30.png", True)},
                              }



        # Set the image the player starts with
        self.image = self.get_frames()[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.shooting = False
        self.max_hp = 50
        self.hp = self.max_hp

        self.shooting_sound_start = pygame.mixer.Sound(utils.get_asset_path('196907__dpoggioli__laser-gun-recharge.wav'))
        self.shooting_sound_continuous = pygame.mixer.Sound(utils.get_asset_path('146725__fins__laser.wav'))

        self.channel_1 = pygame.mixer.Channel(0) # argument must be int
        self.channel_2 = pygame.mixer.Channel(1)

    def reset_state(self):
        self.hp = self.max_hp
        self.stop()
        self.update_state()

    def get_frames(self):
        return self.state_frames[self.state][self.direction]

    def get_walking_frames(self, file_name, flip=False):
        sprite_sheet = SpriteSheet(file_name)
        frames = []
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, flip, False)
        frames.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, flip, False)
        frames.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, flip, False)
        frames.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, flip, False)
        frames.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, flip, False)
        frames.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, flip, False)
        frames.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, flip, False)
        frames.append(image)
        return frames


    def take_damage(self, damage):
        print("taking damage hp", damage)

        self.hp -= damage

        print("new hp", self.hp)

        self.update_state()
        self.set_state(P_STATE_DAMAGE)

        self.change_y = -45
        self.change_x = -5
        self.is_dead()

    def is_dead(self):
        if self.hp <= 1:
            print("DEAD!")
            level_manager = LevelManager()
            level_manager.queue_next_level("DeathScreen")


    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.get_frames())
            self.image = self.get_frames()[frame]
        else:
            frame = (pos // 30) % len(self.get_frames())
            self.image = self.get_frames()[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.solid_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            proportional_damage = enemy.max_hp // self.max_hp
            if proportional_damage < 1:
                proportional_damage = 1
            print("taking damage", proportional_damage)
            self.take_damage(proportional_damage)
            break

        exit_hit_list = pygame.sprite.spritecollide(self, self.level.exit_list, False)
        for exit in exit_hit_list:
            self.level.proceed_to_next_level()
            break

        collectible_hit_list = pygame.sprite.spritecollide(self, self.level.collectible_list, False)
        for collectible in collectible_hit_list:

            self.level.money.add_money(collectible.value)
            collectible.kill()
            break


        # Move up/down
        # print("changey", self.change_y)
        # print("changex", self.change_x)
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.solid_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            # if isinstance(block, MovingPlatform):
            #     self.rect.x += block.change_x

        # Bullets
        if self.shooting:
            bullet_x = self.rect.x + 70
            if self.direction == "L":
                bullet_x = self.rect.x - 70
            # print(self.rect.x, self.rect.y)
            bullet = SimpleBullet(bullet_x, self.rect.y + 40, self.direction, self.level)
            self.level.add_bullet(bullet)




    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 4.81

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0

            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height
            if self.state == P_STATE_DAMAGE:
                self.change_x = 0
                self.update_state()

    def set_state(self, state):
        if self.old_state == state:
            return

        self.old_state = self.state
        self.state = state

    def update_state(self):

        relative_hp = 100 * self.hp / self.max_hp
        if isinstance(self.level,Level):
            self.level.health_bar.update_hp(relative_hp)
        print("relativehp", relative_hp)
        if relative_hp > 90:
            self.state = P_STATE_NORMAL
        elif relative_hp > 50:
            self.state = P_STATE_NORMAL_90
        elif relative_hp > 30:
            self.state = P_STATE_NORMAL_50
        else:
            self.state = P_STATE_NORMAL_30

    def shoot(self):
        if self.state == P_STATE_DAMAGE:
            return

        self.set_state(P_STATE_SHOOTING)
        self.shooting = True
        self.channel_1.set_volume(1)
        self.channel_2.set_volume(1)
        self.channel_1.play(self.shooting_sound_start, 0)
        self.channel_2.play(self.shooting_sound_continuous, -1)
        # print("SHOOOTING")

    def stop_shooting(self):
        self.update_state()
        # print("done shootin ")
        self.shooting = False
        self.channel_1.stop()
        self.channel_2.stop()

    def is_shooting(self):
        return self.shooting;

    def jump(self):
        """ Called when user hits 'jump' button. """
        self.update_state()


        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.solid_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -45

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0