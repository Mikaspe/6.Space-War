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

        self.style = style

        self.gunfire_upgrade = 3
        self.hp_upgrade = 0
        self.speed_upgrade = 0

        self.direction = direction
        self.hp = 3

    def hp_update(self):
        self.hp = 3 + self.hp_upgrade

    def speed_update(self):
        self.speed = 4 + 2*self.speed_upgrade

    def gunfire_update(self):
        if self.gunfire_upgrade == 0:
            self.shoot_ratio = 25
            self.weapon_style = 0
        elif self.gunfire_upgrade == 1:
            self.shoot_ratio = 17
            self.weapon_style = 0
        elif self.gunfire_upgrade == 2:
            self.shoot_ratio = 10
            self.weapon_style = 0
        elif self.gunfire_upgrade == 3:
            self.shoot_ratio = 20
            self.weapon_style = 1

    def reset(self):
        self.gunfire_upgrade = 3
        self.hp_upgrade = 0
        self.speed_upgrade = 0
