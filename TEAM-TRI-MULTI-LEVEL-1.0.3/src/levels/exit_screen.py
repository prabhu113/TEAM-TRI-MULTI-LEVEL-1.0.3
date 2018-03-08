from src.levels.game_screen import *
from src.level_manager import *
from src.spritesheet_functions import *
from src.menu_display import *
import src.utils

class ExitScreen(Screen, MenuDisplay):
    def __init__(self):
        super(ExitScreen, self).__init__()
        LevelManager().exit()

    def update(self):
        self.leave()

    def prepare_assets(self):
        pass
    def handle_keyboard_event(self, event):
        pass
    @staticmethod
    def get_menu_name():
        return "Exit"










