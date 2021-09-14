import pygame
from CONST import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, style):

        pygame.sprite.Sprite.__init__(self)  # potrzebne ? !!!!!!!!!!!
        if style == 'player':
            self.image = pygame.image.load('img/projectile-player.png').convert_alpha()
        elif style == 'enemy':
            self.image = pygame.image.load('img/projectile-enemy.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.rect.x = x
        self.rect.y = y

        self.type = style

    def move(self):
        if self.type == 'player':
            self.rect.y -= PROJECTILE_SPEED
        else:
            self.rect.y += PROJECTILE_SPEED
