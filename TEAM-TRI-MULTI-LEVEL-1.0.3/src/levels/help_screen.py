from src.levels.game_screen import *
from src.level_manager import *
from src.spritesheet_functions import *
from src.menu_display import *


class HelpScreen(Screen, MenuDisplay):
    def __init__(self):
        super(HelpScreen, self).__init__()

        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self._text = "HELP\n\n " \
                     "How to play\n\n" \
                     "MOVE\n" \
                     "LEFT/RIGHT\n\n" \
                     "JUMP\n" \
                     "UP\n\n\n" \
                     "SHOOT\n" \
                     "SPACE\n\n\n" \
                     "Main Menu\n\n" \
                     "m: change music\n\n" \
                     "ESC\n" \
                     "quit current screen/game"


        self.moving_text_speed = 5
        self.text_y = SCREEN_HEIGHT + 20

    def restart_music(self):
        MusicManager().prepare(MUSIC_HELP)
        MusicManager().play()

    def view_did_appear(self):
        self.restart_music()

    def prepare_assets(self):

        pass

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            # An argument can be made to place leaving the level in the main loop
            super(HelpScreen, self).view_did_appear()
            if event.key == pygame.K_ESCAPE:
                self.leave()
            elif event.key == pygame.K_p:
                self.leave()

    # No need to do anything here, unless we've got some animation
    def update(self):
        pass

    @staticmethod
    def get_menu_name():
        return "Help"

    def draw(self, screen):
        # Clear the screen
        # screen.fill(constants.BLACK)

        utils.blit_text_centered(screen, self._text, (SCREEN_WIDTH // 2, self.text_y), self.font)
        # screen.blit(self._text, [250, self.text_y])

        if self.text_y >= 50:
            self.text_y -= self.moving_text_speed

        if self.text_y >= 850:
            self.text_y = -50








