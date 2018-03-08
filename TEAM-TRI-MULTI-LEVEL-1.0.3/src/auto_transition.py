# Abstract class, making sure that all subclasses at least attempt
# to implement the update, draw, and handle_keyboard_event methods

from src.constants import *

import pygame

class AutoTransition:

    def start_auto_transition(self):
        self.time_since_start = pygame.time.get_ticks()

    def check_auto_transition(self):
        seconds = (pygame.time.get_ticks() - self.time_since_start) / 1000
        if seconds > self.ttl:
            self.leave()

