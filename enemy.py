import pygame
from CONST import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, style, direction='right'):

        pygame.sprite.Sprite.__init__(self)  # potrzebne ? !!!!!!!!!!!

        self.image = pygame.image.load('img/enemy' + str(style) + '.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.rect.centerx = x
        self.rect.centery = y + 40

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
            self.rect.x -= ENEMY_SPEED
        else:
            self.rect.x += ENEMY_SPEED

