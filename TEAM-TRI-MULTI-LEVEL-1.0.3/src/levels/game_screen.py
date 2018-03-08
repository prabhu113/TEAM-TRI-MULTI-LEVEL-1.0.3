import pygame
from src import constants
from src.level import Level
from src.block import *

from src.screen import *
import utils
from pytmx import *
from src.menu_display import *
from src.music_manager import MusicManager
from src.level_manager import LevelManager
import random

class GameScreen(Level, MenuDisplay):
    def __init__(self, file_name=None):
        # Not good practice! Should be a separate object
        self._size = 50
        self._rect_x = 50
        self._rect_y = 50
        self._rect_change_x = 2
        self._rect_change_y = 2
        self.tiled_map = None
        if file_name is None:
            file_name = LevelManager().fetch_next_level()
        self.file_name = file_name
        print("WILL LOAD", file_name)
        super(GameScreen, self).__init__()

    @staticmethod
    def get_menu_name():
        return "Play"

    def view_did_appear(self):
        MusicManager().prepare(MUSIC_LEVEL)
        MusicManager().play(-1, 0.2)

    def prepare_assets(self):
        # self.background = pygame.image.load(utils.get_asset_path("background_01.png")).convert()
        # self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        self.tiled_map = load_pygame(utils.get_asset_path(self.file_name))
        print(self.tiled_map)

        tile_width = self.tiled_map.tilewidth
        tile_height = self.tiled_map.tileheight
        map_width = self.tiled_map.width * tile_width
        map_height = self.tiled_map.height * tile_height

        self.world_offset_y = constants.SCREEN_HEIGHT - map_height

        order = 1
        for layer in self.tiled_map.layers:
            order += 1
            zindex = 200
            # zindex = order

            paralax = 1
            if "zindex" in layer.properties:
                zindex = int(layer.zindex)

            if "paralax" in layer.properties:
                paralax = int(layer.paralax)+1


            # paralax = order

            # print("layer name", layer.name, "order", order, "zindex", zindex, "paralax vaue", paralax, zindex)
            if isinstance(layer, TiledTileLayer):

                for x, y, image in layer.tiles():
                    # sprite = Block(image, x*tile_width, y*tile_height + self.world_offset_y)
                    sprite = Block(image.convert_alpha(), x * tile_width, y * tile_height + self.world_offset_y)
                    if "background" in layer.properties and layer.properties['background'] == "true":
                        sprite._layer = zindex
                        if "solid" in layer.properties and layer.properties['solid'] == "true":
                            self.add_solid_sprite(sprite)
                        else:
                            self.add_background_sprite(sprite)

            elif isinstance(layer, TiledObjectGroup):
                for object in layer:
                    if "solid" in layer.properties and layer.solid == "true":
                        sprite = Block(object.image.convert_alpha(), object.x, object.y + self.world_offset_y)
                        sprite._layer = zindex
                        self.add_solid_sprite(sprite)
                    elif "enemy" in layer.properties and layer.enemy == "true":
                        hp = randint(20, 50)
                        if "hp" in layer.properties:
                            hp = int(layer.properties['hp'])

                        can_shoot = bool(random.getrandbits(1))
                        if "can_shoot" in layer.properties:
                            can_shoot = True if layer.properties['can_shoot'] == "true" else False


                        can_jump = bool(random.getrandbits(1))
                        if "can_jump" in layer.properties:
                            can_jump = True if layer.properties['can_jump'] == "true" else False



                        sprite = Enemy(self.get_images_from_object(self.tiled_map, object), object.x, object.y + self.world_offset_y, hp)
                        sprite.can_shoot = can_shoot
                        sprite.can_jump = can_jump
                        sprite.level = self
                        self.add_enemy(sprite)
                        print("adding enemy")

                    elif "collectible" in layer.properties:
                        sprite = Collectible(object.image.convert_alpha(), object.x, object.y + self.world_offset_y, 200)
                        sprite._layer = zindex + 200
                        self.add_collectible(sprite)
                        print("adding collectible")

                    elif "exit_condition" in layer.properties:
                        print("adding exit")
                        sprite = ExitBlock(object.image.convert_alpha(), object.x, object.y + self.world_offset_y)
                        sprite._layer = zindex + 200
                        self.add_exit(sprite)
                    else:
                        # print("PARALAX ", paralax)
                        sprite = ParalaxBlock(object.image.convert_alpha(), object.x, object.y + self.world_offset_y, paralax)
                        sprite._layer = zindex
                        self.add_background_sprite(sprite)


    def get_images_from_object(self, map, object):
        images = []
        for frame in object.properties['frames']:
            # do something with the gid and duration of the frame
            # this may change in the future, as it is a little awkward now
            image = map.get_tile_image_by_gid(frame.gid)
            duration = frame.duration
            images.append(image)

        if len(images) < 1:
            images.append(object.image)

        return images

    def proceed_to_next_level(self):
        super(GameScreen, self).proceed_to_next_level()
        file_name = LevelManager().fetch_next_level()
        if file_name is None:
            LevelManager().queue_next_level("CreditScreen")
        else:
            LevelManager().queue_next_level("GameScreen", file_name)
        self.leave()

    def handle_keyboard_event(self, event):
        super(GameScreen, self).handle_keyboard_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.leave()

    def update(self):
        super(GameScreen, self).update()

    def draw(self, screen):
        # Clear the screen
        # screen.fill(constants.BLACK)
        super(GameScreen, self).draw(screen)

