import os

import pygame

from CONST import *


class Player(pygame.sprite.Sprite):
    """Player's spaceship object"""
    def __init__(self, style: str, hp_base: int = 3, speed_base: float = 4, shoot_ratio: float = 20) -> None:
        super().__init__()

        self.style = style
        self.hp_base = hp_base
        self.hp = hp_base
        self.speed_base = speed_base
        self.speed = speed_base
        self.shoot_ratio = shoot_ratio
        self.direction = 'stop'
        self.weapon_style = 1
        self.gunfire_upgrade = 0
        self.hp_upgrade = 0
        self.speed_upgrade = 0
        self.projectiles = []

        self.textures = {}
        for img in os.listdir('../resources/img/Player'):  # Loading all player spaceships images
            self.textures[img.replace('.png', '')] = pygame.image.load(f'../resources/img/player/{img}').convert_alpha()

        self.image = self.textures[f'{self.style}-{self.direction}']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(DRAW_SCREEN_SIZE[0]/2, DRAW_SCREEN_SIZE[1]-75))

    def gunfire_update(self) -> None:
        """Updates player shoot ratio and weapon style depending on actual 'gunfire_upgrade' level.
        Called before each game level."""
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

    def hp_update(self) -> None:
        """Updates player HP.
        Called before each game level."""
        self.hp = self.hp_base + self.hp_upgrade

    def speed_update(self) -> None:
        """Updates player speed.
        Called before each game level."""
        self.speed = self.speed_base + 2*self.speed_upgrade

    def reset(self) -> None:
        """Resets all upgrades.
        Called before starting a game."""
        self.gunfire_upgrade = 0
        self.hp_upgrade = 0
        self.speed_upgrade = 0

    def change_spaceship(self, style: str) -> None:
        """Changes spacheship model.
        Called when player decide to change model in 'Spaceship choose' menu before game"""
        self.style = style
        self.image = self.textures[f'{self.style}-{self.direction}']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(DRAW_SCREEN_SIZE[0]/2, DRAW_SCREEN_SIZE[1]-75))

    def get_image(self) -> pygame.Surface:
        """Returns and updates current spaceship image with proper direction(left, right or stop).
        Called in 'draw_game' method"""
        self.image = self.textures[f'{self.style}-{self.direction}']
        return self.image
