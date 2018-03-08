from src.levels.game_screen import *
from src.level_manager import *
from src.menu_display import *


class DeathScreen(Screen, MenuDisplay):
    def __init__(self):
        super(DeathScreen, self).__init__()

        self.jumbo_font = pygame.font.SysFont('Calibri', 50, True, False)
        self.font = pygame.font.SysFont('Calibri', 25, True, False)

        self._text_1 = "YOU DIED"
        self.text_1_y = SCREEN_HEIGHT + 20

        self._text_2 = "Press ENTER to Restart\n" \
                       "Press ESC to go back to MAIN MENU"
        self.text_2_y = SCREEN_HEIGHT + 70

        self.moving_text_speed = 5
        self.background = pygame.image.load(utils.get_asset_path('igor_death_bg.jpg'))

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
            super(DeathScreen, self).view_did_appear()
            if event.key == pygame.K_ESCAPE:
                self.leave()
            elif event.key == pygame.K_RETURN:
                level_manager = LevelManager()
                level_manager.reset_player_state()
                level_manager.queue_next_level("GameScreen")

    @staticmethod
    def get_menu_name():
        return "Death"

    def draw(self, screen):
        # Clear the screen
        # screen.fill(constants.BLACK)

        screen.blit(self.background, [0, 0])

        utils.blit_text_centered(screen, self._text_1, (SCREEN_WIDTH // 2, self.text_1_y), self.jumbo_font)
        utils.blit_text_centered(screen, self._text_2, (SCREEN_WIDTH // 2, self.text_2_y), self.font)

        if self.text_1_y >= 350:
            self.text_1_y -= self.moving_text_speed

        if self.text_1_y >= 850:
            self.text_1_y = -50

        if self.text_2_y >= 400:
            self.text_2_y -= self.moving_text_speed

        if self.text_2_y >= 850:
            self.text_2_y = -50
