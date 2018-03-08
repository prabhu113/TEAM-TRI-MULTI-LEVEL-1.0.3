from src.levels.game_screen import *
from src.level_manager import *
from src.menu_display import *
from src.spritesheet_functions import *
from src.persist_stack import *
import random
from src.music_manager import MusicManager
from src import utils
from random import randint
import math



class MainMenu(Screen, PersistStack):
    def __init__(self):

        self.text_location_x = constants.SCREEN_WIDTH / 2 - 345
        # self.static_text_location_x = self.text_location_x
        self.y_bounce = self.text_location_x

        # Dynamic Text logic
        self.y_bounce_right = True
        self.y_bounce_left = False
        self.blocks = 10
        self.snow_list = []
        self.glitch = False
        self.glitch_time = pygame.time.get_ticks()

        for i in range(50):
            x_val = random.randrange(-10, constants.SCREEN_WIDTH + 10)
            y_val = random.randrange(-10, constants.SCREEN_HEIGHT + 10)
            self.snow_list.append([x_val, y_val])

        self.font_size = 35
        self.font = pygame.font.SysFont('Calibri', self.font_size, True, False)
        self.small_font = pygame.font.SysFont('Calibri', 10, True, False)
        self.jumbo_font = pygame.font.SysFont('Calibri', 45, True, False)


        # Variables with _ first denotes private variables
        self.control_text_location_x = 300
        self._text = self.small_font.render("UP/DOWN/ENTER to make selection", True, constants.WHITE)
        self.jumbo_text = self.jumbo_font.render("Alien Oddity", True, constants.WHITE)

        self.menu_list = ["GameScreen", "HelpScreen", "CreditScreen", "ExitScreen"]
        self.index = 1

        self.bg_direction_x = -1
        self.bg_direction_y = -1
        self.bg_change_power_x = 0.3
        self.bg_change_power_y = 0.5
        self.bg_glitch = 0
        self.background_x = 0
        self.background_y = 0

        super(MainMenu, self).__init__()
        
        
    def prepare_assets(self):
        MusicManager().prepare(MUSIC_MENU)
        self.background = pygame.image.load(utils.get_asset_path('igor_bg_menu2.jpg'))

        # self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("here1")
        # super(MainMenu, self).prepare_assets()

    def view_did_appear(self):
        self.restart_music()

    def restart_music(self):
        MusicManager().prepare(MUSIC_MENU)
        MusicManager().play()

    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            # An argument can be made to place leaving the level in the main loop
            super(MainMenu, self).view_did_appear()
            if event.key == pygame.K_ESCAPE:
                self.leave()
            elif event.key == pygame.K_RETURN:
                self.go_to_level()
            elif event.key == pygame.K_UP:
                if self.index > 0:
                    self.index -= 1
            elif event.key == pygame.K_DOWN:
                if self.index < len(self.menu_list) - 1:
                    self.index += 1
            elif event.key == pygame.K_m:
                self.restart_music()

    def go_to_level(self):
        level_manager = LevelManager()
        level_manager.reset_player_state()
        level_manager.queue_next_level(self.menu_list[self.index])


    # No need to do anything here, unless we've got some animation
    def update(self):
        if randint(10, 10000) < 20:
            self.glitch = True
            self.bg_glitch = 5 * random.choice([-1,1])
            self.glitch_time = pygame.time.get_ticks()

        self.text_glitch = 0
        if self.glitch and randint(1, 100) < 20:
            self.text_glitch = randint(1, 50)
            if pygame.time.get_ticks() - self.glitch_time > 2000:
                self.glitch = False
                self.bg_glitch = 0

        background_width  = self.background.get_rect().size[0]
        background_height = self.background.get_rect().size[1]

        self.background_x += self.bg_direction_x * (self.bg_change_power_x + self.bg_glitch)
        self.background_y += self.bg_direction_y * (self.bg_change_power_y + self.bg_glitch)
        #self._rect_y += self._rect_change_y

        if (self.background_x + background_width) <= SCREEN_WIDTH or self.background_x > 0:
            self.bg_direction_x *= -1
        if (self.background_y + background_height) <= SCREEN_HEIGHT or self.background_y > 0:
            self.bg_direction_y *= -1


    def view_will_disappear(self):
        MusicManager().fade_out()

    def draw(self, screen):
        super(MainMenu, self).draw(screen)
        # Clear the screen
        # screen.fill(constants.BLACK)
        screen.blit(self.background, [self.background_x, self.background_y])

        for i in range(len(self.snow_list)):
            pygame.draw.circle(screen, constants.WHITE, (self.snow_list[i][0], self.snow_list[i][1]), 2, 0)

            self.snow_list[i][1] += 1
            if self.snow_list[i][1] >= constants.SCREEN_HEIGHT:
                self.snow_list[i][1] = -10
                self.snow_list[i][0] = random.randrange(-10, constants.SCREEN_WIDTH + 10)



        screen.blit(self.jumbo_text, [self.text_location_x, 75 + self.text_glitch])


        if self.text_location_x > 700:
            self.y_bounce_right = False
            self.y_bounce_left = True

        if self.y_bounce_left:
            self.text_location_x -= 2

        if self.text_location_x <= 100:
            self.y_bounce_right = True
            self.y_bounce_left = False

        if self.y_bounce_right:
            self.text_location_x += 2

        i = 0
        y = -100
        for item in self.menu_list:

            each_screen = fetch_static_class(item)
            if not issubclass(each_screen, MenuDisplay):
                continue

            y += 30

            menu_text = each_screen.get_menu_name()

            color = constants.WHITE

            if i == self.index:
                color = constants.RED
            control_text_2 = self.font.render(menu_text, True, color)
            screen.blit(control_text_2, [190, constants.SCREEN_HEIGHT / 2 + y])
            i += 1

        screen.blit(self._text, [20, SCREEN_HEIGHT - 20])