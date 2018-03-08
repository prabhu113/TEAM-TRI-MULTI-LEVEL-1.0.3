from src.levels.game_screen import *
from src.level_manager import *
from src.spritesheet_functions import *
from src.menu_display import *
import src.utils

class CreditScreen(Screen, MenuDisplay):
    def __init__(self):
        super(CreditScreen, self).__init__()

        self.audio_path = '/path/to/your/favorite/song.mp3'
        # todo move this into prepare assets



        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self._text_exit_back = self.font.render("Press 'ESCAPE' to go back", 1, constants.WHITE)
        self._text = "CREDITS\n\n " \
                     "LEAD DEVELOPER\n" \
                     "Igor Mekhtiev\n\n\n\n" \
                     "Developers\n\n" \
                     "Terrance Hanlon\n\n" \
                     "Ryan Wilke" \
                     "\n\n\n\n\n" \
                     "Music\n" \
                     "Ben from https://www.bensound.com\n" \
                     "\n\n\n" \
                     "Gfx Assets\n\n"\
                     "Code Inferno Games: codeinferno.com\n" \
                     "https://opengameart.org/content/3-parallax-backgrounds\n\n\n\n" \
                     "Game art by Ken: http://kenney.nl/assets/platformer-art-extended-enemies\n\n" \
                     "Background photos (C) Igor Mekhtiev\n" \
                     "Game intro\n" \
                     "sounds: Jingle_Win_01.wav & Jingle_Win_00.wav / www.littlerobotsoundfactory.com\n" \
                     "Summer\n"\
                     "https://creativecommons.org/licenses/by/3.0/\n"\
                     "https://freesound.org/people/Dpoggioli/sounds/196907/\n" \
                     "https://freesound.org/people/fins/sounds/146725/\n" \
                     "https://freesound.org/people/Chance4doom/sounds/394213/\n"\
                     "Game intro sounds: Jingle_Win_01.wav & Jingle_Win_00.wav/www.littlerobotsoundfactory.com\n"\
                     "Advendture: www.soundemperor.com\n" \
                     "Additional Libraries\n" \
                     "PyTMX\n" \
                     "Written using PyGame\n\n" \
                     "Press 'ESCAPE' to go back to main menu"



        self.moving_text_speed = 0.3
        self.text_y = SCREEN_HEIGHT + 20

    def restart_music(self):
        MusicManager().prepare(MUSIC_CREDITS)
        MusicManager().play()

    def view_did_appear(self):
        self.restart_music()

    def prepare_assets(self):

        pass

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            # An argument can be made to place leaving the level in the main loop
            super(CreditScreen, self).view_did_appear()
            if event.key == pygame.K_ESCAPE:
                self.leave()
            elif event.key == pygame.K_p:
                self.leave()

    # No need to do anything here, unless we've got some animation
    def update(self):
        pass

    @staticmethod
    def get_menu_name():
        return "Credits"

    def draw(self, screen):
        # Clear the screen
        # screen.fill(constants.BLACK)
        utils.blit_text_centered(screen, self._text, (SCREEN_WIDTH // 2, self.text_y), self.font)
        # screen.blit(self._text, [250, self.text_y])

        self.text_y -= self.moving_text_speed

        if self.text_y >= 850:
            self.text_y = -50








