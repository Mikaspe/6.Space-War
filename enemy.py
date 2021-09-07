import pygame
from CONST import *


class Enemy(pygame.Rect):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.h = 32
        self.w = 32
        self.type = str(type)
        self.direction = 'left'

    def move(self):
        if self.direction == 'left':
            self.x -= ENEMY_SPEED
            if self.x < BORDER:
                self.direction = 'right'
                self.y += 40
        else:
            self.x += ENEMY_SPEED
            if self.x >= DRAW_SCREEN_SIZE[0] - BORDER:
                self.direction = 'left'
                self.y += 40
