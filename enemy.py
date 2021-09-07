import pygame
from CONST import *


class Enemy(pygame.Rect):
    def __init__(self, x, y, type, direction='right'):
        self.x = x
        self.y = y
        self.h = 32
        self.w = 65
        self.type = str(type)
        self.direction = str(direction)

    def move(self):
        if self.direction == 'left':
            self.x -= ENEMY_SPEED
        else:
            self.x += ENEMY_SPEED

