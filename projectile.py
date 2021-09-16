import pygame
from CONST import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, style):

        pygame.sprite.Sprite.__init__(self)  # potrzebne ? !!!!!!!!!!!
        if style == 'player':
            self.image = pygame.image.load('img/projectile-player.png').convert_alpha()
        elif style == 'player-l':
            self.image = pygame.image.load('img/projectile-player-l.png').convert_alpha()
        elif style == 'player-r':
            self.image = pygame.image.load('img/projectile-player-r.png').convert_alpha()
        elif style == 'enemy':
            self.image = pygame.image.load('img/projectile-enemy.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.rect.x = x
        self.rect.y = y

        self.style = style

    def move(self):
        SPEED_X = 0.3
        if self.style == 'player':
            self.rect.y -= PROJECTILE_SPEED
        elif self.style == 'player-l':
            self.rect.y -= PROJECTILE_SPEED
            self.rect.x -= PROJECTILE_SPEED * SPEED_X
        elif self.style == 'player-r':
            self.rect.y -= PROJECTILE_SPEED
            self.rect.x += PROJECTILE_SPEED * SPEED_X
        else:
            self.rect.y += PROJECTILE_SPEED
