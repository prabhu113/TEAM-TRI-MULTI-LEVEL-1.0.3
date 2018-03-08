import os
import pygame

def get_asset_path(file):
    return "assets" + os.path.sep + file


def blit_text_centered(surface, text, center_position, font, color=pygame.Color("gray")):
    lines = text.splitlines()

    x, y = center_position
    for line in lines:
        line_surface = font.render(line, 0, color)
        line_width, line_height = line_surface.get_size()

        x -= line_width // 2

        surface.blit(line_surface, (x, y))
        x = center_position[0]
        y += line_height