#A Singleton object
#http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

from src.levels import *
from src.constants import *
from src.persist_stack import PersistStack

class LevelManager:
    """ The LevelManager's job is to keep a stack of the currently executing screens """

    # Inner class - This is where the implementation goes!
    class __LevelManager:

        def __init__(self):
            self.player = None
            self.incoming_level = None
            self.screen_stack = []
            self.level_hierarchy = ["IntroTitleScreen", "GameTitleScreen", "MainMenu"]
            self.level_hierarchy.reverse()
            for class_name in self.level_hierarchy:
                self.screen_stack.append(fetch_screen(class_name))

            self.sequence_of_levels = ['background_02.tmx', 'background_01.tmx']

            self.original_sequence_of_levels = self.sequence_of_levels
            self.sequence_of_levels.reverse()

        def reset_player_state(self):
            if self.player is not None:
                self.player.reset_state()
                self.reset_sequence_of_levels()

        def set_player(self, player):
            self.player = player

        def exit(self):
            self.incoming_level = None
            self.get_current_level().leave()

        def win(self):
            self


        def tick(self):
            """ Level manager housekeeping """


            " If incoming level is set that means we need to transition "
            current_level = self.get_current_level()
            if self.incoming_level is not None:
                " If incoming level is ready then proceed"
                if self.incoming_level.state == LEVEL_STATE_READY:

                    " If current level is dead then bye-bye"
                    if current_level.state == LEVEL_STATE_DEFUNCT:
                        incoming_level = self.incoming_level
                        self.incoming_level = None
                        self.screen_stack.append(incoming_level)
                        self.screen_stack.remove(current_level)
                    elif current_level.state == LEVEL_STATE_SUSPENDED:
                        incoming_level = self.incoming_level
                        self.incoming_level = None
                        self.screen_stack.append(incoming_level)
                        "if current level state is running then ask it to leave "
                    elif current_level.state == LEVEL_STATE_RUNNING:
                        if not isinstance(current_level, PersistStack):
                            current_level.leave()
                        else:
                            current_level.suspend()

                else:
                    pass
            elif current_level.state == LEVEL_STATE_DEFUNCT:
                self.screen_stack.remove(current_level)
            elif current_level.state == LEVEL_STATE_SUSPENDED:
                current_level.resume()


        def queue_next_level(self, name, file_name = None):
            if file_name is None:
                self.incoming_level = fetch_screen(name)
            else:
                self.incoming_level = fetch_screen(name, file_name)



        def add_level(self, level):
            self.screen_stack.append(level)


        def next(self):
            pass

        def get_current_level(self):
            """ Returns the current visible level """
            return (self.screen_stack or [None])[-1]

        def fetch_next_level(self):
            """ TODO """
            file_name = (self.sequence_of_levels or [None])[-1]
            self.sequence_of_levels = self.sequence_of_levels[:-1]
            return file_name

        def reset_sequence_of_levels(self):
            self.sequence_of_levels = self.original_sequence_of_levels


    # Instance variable!
    instance = None

    def __init__(self):
        # Create an object if one does not exist
        # Note that if two constructors are called, only one object is created!
        if not LevelManager.instance:
            LevelManager.instance = LevelManager.__LevelManager()

    # Pass attribute retrieval to the instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
