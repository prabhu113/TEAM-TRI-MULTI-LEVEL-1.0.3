from src.levels.game_screen import *
from src import utils


class GameTitleScreen(Screen, AutoTransition):

    def __init__(self):
        """ Call parent constructor to setup necessary stuff """
        super(GameTitleScreen, self).__init__()


    def view_did_appear(self):
        print("View did appear")
        super(GameTitleScreen, self).view_did_appear()
        self.start_auto_transition()
        self.background_sound.play()

    def view_did_disappear(self):
        self.background_sound.stop()

    def prepare_assets(self):
        """ This is where you should be loading all your assets/fonts/images etc..."""
        self.ttl = 5  # TTL in seconds
        self.background = pygame.image.load(utils.get_asset_path('Alien Oddity.png'))
        self.background_sound = pygame.mixer.Sound(utils.get_asset_path('game_title_sound.ogg'))

        # Because this text never changes, we can load it in the constructor
        # Otherwise, we may need to move render into draw
        #font = pygame.font.SysFont('Calibri', 25, True, False)

        # The underscore character indicates that this is a private instance variable
        #self._text = font.render("Otto's eating frenzy...", True, constants.BLACK)

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            # An argument can be made to place leaving the level in the main loop
            if event.key == pygame.K_ESCAPE:
                self.leave()

    # No need to do anything here, unless we've got some animation
    def update(self):
        """ Update game logic here """
        pass

    def draw(self, screen):
        # Clear the screen
        screen.fill(constants.WHITE)

        # Draw my title text!
        screen.blit(self.background, [0, 0])
