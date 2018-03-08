#A Singleton object
#http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

from src.levels import *
from src.constants import *
from src.persist_stack import PersistStack
import random
import pygame
from src import utils


class MusicManager:
    """ The LevelManager's job is to keep a stack of the currently executing screens """

    # Inner class - This is where the implementation goes!
    class __MusicManager:

        def __init__(self):
            self.music_playing = False
            self.incoming_level = None
            self.screen_stack = []
            self.level_tracks = ["bensound-downtown.mp3", "bensound-badass.mp3"]
            self.menu_tracks = ["bensound-sexy.mp3", "bensound-groovyhiphop.mp3", "bensound-scifi.mp3"]
            self.paused_tracks = [""]
            self.help_tracks = ["bensound-sweet.mp3"]
            self.credits_tracks = ["bensound-memories.mp3", "bensound-romantic.mp3"]
            self.background_music = None
            self.background_music_pending = None

            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)

            # This is the sound channel
            self.music_channel = pygame.mixer.Channel(CHANNEL_MUSIC)
            self.filename = None

            self.music = {MUSIC_CREDITS: self.credits_tracks,
                          MUSIC_MENU: self.menu_tracks,
                          MUSIC_LEVEL: self.level_tracks,
                          MUSIC_PAUSED: self.paused_tracks,
                          MUSIC_HELP: self.help_tracks}

        @staticmethod
        def get_random_track_from_stack(stack):
            return random.choice(stack)

        def prepare(self, music_type):
            stack = self.music[music_type]
            self.filename = utils.get_asset_path(self.get_random_track_from_stack(stack))
            self.background_music_pending = pygame.mixer.music.load(self.filename)


        def fade_out(self):
            pygame.mixer.music.fadeout(500)

        def play_menu(self):
            self.prepare(self.menu_tracks)
            self.play()

        def play(self, param=-1, volume = 1):
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(param)



    # Instance variable!
    instance = None



    def __init__(self):
        # Create an object if one does not exist
        # Note that if two constructors are called, only one object is created!
        if not MusicManager.instance:
            MusicManager.instance = MusicManager.__MusicManager()

    # Pass attribute retrieval to the instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
