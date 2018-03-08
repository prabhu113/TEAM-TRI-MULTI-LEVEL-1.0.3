
"""
Alien Oddity by Team TRI

Version: 2018-FEB-19

Please refer to Credits Screen for GFX and SFX Credits.

"""

import pygame
from src import constants
from src.level_manager import *
from src.player import Player
from src.playable import Playable



# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode([constants.SCREEN_WIDTH,
                                constants.SCREEN_HEIGHT],
                                pygame.DOUBLEBUF |
                                pygame.HWSURFACE |
                                pygame.HWACCEL
                                | pygame.FULLSCREEN
                                 )
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
level_manager = LevelManager()

# Create the player
player = Player()
player.rect.x = 540
player.rect.y = constants.SCREEN_HEIGHT - player.rect.height

level_manager.set_player(player)

done = False

# -------- Main Program Loop -----------
while not done:
    level_manager.tick()
    current_level = level_manager.get_current_level()

    # We've left the TitleScreen - Exit the game
    if current_level is None:
        break


    # todo move this out this is ugly

    if isinstance(current_level, Playable):
        current_level.set_player(player)

    player.level = current_level

    # eof todo

    # Needs Game Logic
    screen.fill(constants.BLACK)

    for event in pygame.event.get():
        current_level.handle_keyboard_event(event)
        if event.type == pygame.QUIT:
            done = True
            break


    # Update the player.
    current_level.fire_events()
    current_level.update()

    # Draw logic
    current_level.draw(screen)

    # Update the screen with what we've drawn.
    pygame.display.update()
 
    # Limit to 60 frames per second
    clock.tick(60)


pygame.quit()
