import pygame
from CONST import *


class Player(pygame.sprite.Sprite):
    def __init__(self, style, direction='stop'):

        pygame.sprite.Sprite.__init__(self)  # potrzebne ? !!!!!!!!!!!
        self.image = pygame.image.load('img/player1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(0, 0))


        self.rect.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.rect.y = DRAW_SCREEN_SIZE[1] - self.rect.h - 20

        self.direction = direction
        self.hp = 3
