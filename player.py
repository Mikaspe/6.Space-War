import pygame
from CONST import *


class Player(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.y = 550
        self.h = 85
        self.w = 124
        self.hp = 3