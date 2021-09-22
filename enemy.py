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

        self.style = style
        self.direction = str(direction)
        self.hp = 1
        self.speed = 2


        if style == 1:
            self.hp = 1
            self.shoot_ratio = 150
        elif style == 2:
            self.hp = 5
            self.shoot_ratio = 200
        elif style == 3:
            self.hp = 3
            self.shoot_ratio = 100
        elif style == 4:
            self.hp = 3
            self.shoot_ratio = 100

    def move(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

