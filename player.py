import pygame
from CONST import *

class Player(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.y = 230
        self.h = 85
        self.w = 124
