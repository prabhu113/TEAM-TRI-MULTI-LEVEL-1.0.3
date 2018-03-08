# Abstract class, making sure that all subclasses at least attempt
# to implement the update, draw, and handle_keyboard_event methods

from src.constants import *
from src.auto_transition import *
import pygame

class Screen:
    def __init__(self):
        """ Make sure to call super in children"""
        self.state = LEVEL_STATE_NEW
        self.is_loaded = False


        # Background image
        self.background = None


        # Events
        self.view_will_load()
        self.prepare_assets()
        self.view_did_load()

    def view_will_load(self):
        """ Called before assets are loaded"""
        pass

    def view_did_load(self):
        """ Called immediately after the screen assets are loaded """
        self.is_loaded = True
        self.state = LEVEL_STATE_READY

    def prepare_assets(self):
        """ This is where you should be loading all your assets/fonts/images etc..."""
        raise NotImplementedError

    def is_visible(self):
        if self.state == LEVEL_STATE_RUNNING:
            return True
        return False

    def view_did_appear(self):
        pass

    def view_will_disappear(self):
        pass

    def view_did_disappear(self):
        pass

    def handle_keyboard_event(self, event):
        raise NotImplementedError

    def fire_events(self):
        if self.state == LEVEL_STATE_READY:
            self.state = LEVEL_STATE_RUNNING
            self.view_did_appear()

        if isinstance(self, AutoTransition):
            self.check_auto_transition()

    def update(self):
        pass
        """ Update game logic here """

        
    def draw(self, screen):
        pass

    def suspend(self):
        self.state = LEVEL_STATE_IN_TRANSITION
        self.view_will_disappear()
        self.view_did_disappear()
        self.state = LEVEL_STATE_SUSPENDED

    def resume(self):
        self.state = LEVEL_STATE_IN_TRANSITION
        self.view_did_appear()
        self.state = LEVEL_STATE_RUNNING

    def leave(self):
        self.state = LEVEL_STATE_IN_TRANSITION
        self.view_will_disappear()
        self.view_did_disappear()
        self.state = LEVEL_STATE_DEFUNCT
