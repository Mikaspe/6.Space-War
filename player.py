import pygame
import os
from CONST import *


class Player(pygame.sprite.Sprite):
    def __init__(self, style, hp_base=3, speed_base=4, shoot_ratio=20):
        super().__init__()

        self.style = style
        self.direction = 'stop'
        self.hp_base = hp_base
        self.hp = hp_base
        self.speed_base = speed_base
        self.speed = speed_base
        self.shoot_ratio = shoot_ratio
        self.weapon_style = 1
        self.gunfire_upgrade = 0
        self.hp_upgrade = 0
        self.speed_upgrade = 0

        self.textures = {}
        for img in os.listdir('img/player'):  # Loading all player spaceships images
            self.textures[img.replace('.png', '')] = pygame.image.load(f'img/player/{img}')  # => surface

        self.image = self.textures[f'{self.style}-{self.direction}']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (DRAW_SCREEN_SIZE[0] / 2, DRAW_SCREEN_SIZE[1] - 75)

    def hp_update(self):
        self.hp = self.hp_base + self.hp_upgrade

    def speed_update(self):
        self.speed = self.speed_base + 2*self.speed_upgrade

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
        self.gunfire_upgrade = 0
        self.hp_upgrade = 0
        self.speed_upgrade = 0

    def get_image(self):
        self.image = self.textures[f'{self.style}-{self.direction}']
        return self.image
