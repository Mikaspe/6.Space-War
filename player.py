import pygame
from CONST import *


class Player(pygame.Rect):
    def __init__(self, style, size, direction='stop'):
        self.w = size[0]
        self.h = size[1]
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.y = DRAW_SCREEN_SIZE[1] - self.h - 20
        self.direction = direction
        self.hp = 3
