import pygame
from CONST import *


class Enemy(pygame.Rect):
    def __init__(self, x, y, style, size, direction='right'):
        self.x = x
        self.y = y
        self.w = size[0]
        self.h = size[1]
        self.type = str(style)
        self.direction = str(direction)
        self.hp = 1

        if style == 1:
            self.hp = 1
        elif style == 2:
            self.hp = 5
        elif style == 3:
            self.hp = 3
        elif style == 4:
            self.hp = 1000

    def move(self):
        if self.direction == 'left':
            self.x -= ENEMY_SPEED
        else:
            self.x += ENEMY_SPEED

