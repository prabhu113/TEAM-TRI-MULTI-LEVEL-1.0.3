"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame
from src import utils
from src import constants

from src.level_manager import *
from src.level import *
from random import randint


class AnimatedBlock(pygame.sprite.Sprite):
    """ Animated Block. """

    # -- Methods
    def __init__(self, frames, x, y):
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
        self.direction = "L"

        self.money = 0

        # List of sprites we can bump against
        self.level = None

        self.state_frames = {}

        self.set_frames_for_state(P_STATE_NORMAL, frames)

        # Set the image the player starts with
        self.image = self.get_frames()[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.shooting = False
        self.max_hp = 100
        self.hp = self.max_hp

        self.shooting_sound_start = pygame.mixer.Sound(utils.get_asset_path('196907__dpoggioli__laser-gun-recharge.wav'))
        self.shooting_sound_continuous = pygame.mixer.Sound(utils.get_asset_path('146725__fins__laser.wav'))

        self.channel_1 = pygame.mixer.Channel(0) # argument must be int
        self.channel_2 = pygame.mixer.Channel(1)

        self.rect.x = x
        self.rect.y = y

        #for gliding
        self.start_y = y
        self.change_in_y = 1
        self.jump_up = True

    def set_frames_for_state(self, state, frames):
        if state not in self.state_frames:
            self.state_frames[state] = {}

        self.state_frames[state]["L"] = frames
        self.state_frames[state]["R"] = []
        for frame in frames:
            self.state_frames[state]["R"].append(pygame.transform.flip(frame, True, False))


    def reset_state(self):
        self.hp = self.max_hp
        self.stop()
        self.update_state()

    def get_frames(self):
        state = self.state
        if self.state not in self.state_frames:
            state = P_STATE_NORMAL

        return self.state_frames[state][self.direction]


    def take_damage(self, damage):
        print("taking damage hp", self.hp)

        self.hp -= damage

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


    def update(self, args):
        super(AnimatedBlock, self).update(args)
        # """ Move the player. """
        # # Gravity

        pos = pygame.time.get_ticks() // 3 #self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.get_frames())
            self.image = self.get_frames()[frame]
        else:
            frame = (pos // 30) % len(self.get_frames())
            self.image = self.get_frames()[frame]

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
        self.channel_1.set_volume(0.1)
        self.channel_2.set_volume(0.1)
        self.channel_1.play(self.shooting_sound_start, 0)
        self.channel_2.play(self.shooting_sound_continuous, -1)

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

        self.change_y = -45

    def glide(self):
        if self.change_in_y == 40:
            self.jump_up = False
        if not self.jump_up:
            self.rect.y += 5
            self.change_in_y -= 1
        if self.change_in_y == -10:
            self.jump_up = True
        if self.jump_up:
            self.rect.y -= 5
            self.change_in_y += 1

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0