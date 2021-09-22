import pygame
from CONST import *
import random

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, style):

        pygame.sprite.Sprite.__init__(self)  # potrzebne ? !!!!!!!!!!!
        if style == 'player':
            self.image = pygame.image.load('img/projectile-player.png').convert_alpha()
        elif style == 'player-l':
            self.image = pygame.image.load('img/projectile-player-l.png').convert_alpha()
        elif style == 'player-r':
            self.image = pygame.image.load('img/projectile-player-r.png').convert_alpha()
        elif style.startswith('enemy'):
            self.image = pygame.image.load('img/projectile-enemy.png').convert_alpha()
        elif style.startswith('ball'):
            self.image = pygame.image.load('img/projectile-bal.png').convert_alpha()
        elif style.startswith('smallball'):
            self.image = pygame.image.load('img/projectile-smallbal.png').convert_alpha()

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
        elif self.style == 'enemy1':
            self.rect.y += PROJECTILE_SPEED
        elif self.style == 'enemy2':
            self.rect.y += PROJECTILE_SPEED - 5
        elif self.style == 'enemy3':
            self.rect.y += PROJECTILE_SPEED + 5
        elif self.style == 'enemy4':
            self.rect.y += PROJECTILE_SPEED + 5
        elif self.style == 'ball':
            self.rect.y += PROJECTILE_SPEED - 5

            #self.rect.x += PROJECTILE_SPEED * random.randint(-3, 3) * 0.2


        elif self.style == 'smallball':
            self.rect.y += PROJECTILE_SPEED
