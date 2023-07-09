import pygame
import math

from os.path import join

pygame.init()


def load_image(*paths: (str), convert_alpha: bool = False) -> pygame.Surface:
    if convert_alpha:
        return pygame.image.load(join(*paths)).convert_alpha()
    else:
        return pygame.image.load(join(*paths)).convert()


def direction(x1, x2, y1, y2) -> float:
    dx = x1 - x2
    dy = y1 - y2

    return math.atan2(dx, dy)
