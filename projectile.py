import pygame
from CONST import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, style):

        self.style = style
        pygame.sprite.Sprite.__init__(self)  # potrzebne ? !!!!!!!!!!!

        pygame.image.load('img/projectile/' + self.style).convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.rect.centerx = x
        self.rect.centery = y


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
        elif self.style == 'enemy1':
            self.rect.y += PROJECTILE_SPEED
        elif self.style == 'enemy2':
            self.rect.y += PROJECTILE_SPEED - 5
        elif self.style == 'enemy3':
            self.rect.y += PROJECTILE_SPEED + 5
        elif self.style == 'enemy4':
            self.rect.y += PROJECTILE_SPEED + 5
        elif self.style == 'enemy-ball':
            self.rect.y += PROJECTILE_SPEED - 5
        elif self.style == 'enemy-smallball':
            self.rect.y += PROJECTILE_SPEED
