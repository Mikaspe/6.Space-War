import random

import pygame

from space_war.game_objects.projectile import Projectile


class Enemy(pygame.sprite.Sprite):
    """Enemy spaceship object"""
    def __init__(self, data, pos_x: int, pos_y: int, style: int, direction: str = 'right') -> None:
        super().__init__()
        self.data = data

        self.style = style
        self.direction = direction
        self.speed = 0.1

        self.border = 10 if style == 4 else 60
        self.image = pygame.image.load(f'../resources/img/enemy/enemy{self.style}.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)  # Useful for fast pixel perfect collision detection
        self.rect = self.image.get_rect(center=(pos_x + self.border, pos_y + 40))

        if style == 1:
            self.hp = 1
            self.shoot_ratio = 500
        elif style == 2:
            self.hp = 5
            self.shoot_ratio = 160
        elif style == 3:
            self.hp = 3
            self.shoot_ratio = 100
        elif style == 4:
            self.hp = 400
            self.shoot_ratio = 120
            self.speed = 0.2

        self.played_berserker_sound = False

    def update(self, dt) -> None:
        """Moving enemy in specified direction with defined speed(self.speed).
        Called when pygame event is 'ENEMYMOVE'.
        """
        if self.direction == 'left':
            self.rect.x -= round(self.speed * dt)
        elif self.direction == 'right':
            self.rect.x += round(self.speed * dt)

    def projectile_generation(self, dt):
        """Generating enemy projectiles with definied probability."""
        projectiles = []
        if self.style < 4:
            if random.randint(1, self.shoot_ratio) == 1:
                self.data.SFX['laser-enemy'].play()
                projectile = Projectile(self.rect.centerx, self.rect.centery, f'enemy{self.style}')
                projectiles.append(projectile)
                if self.style == 3:
                    projectile = Projectile(self.rect.centerx - 24, self.rect.centery + 20, 'enemy3')
                    projectiles.append(projectile)
                    projectile = Projectile(self.rect.centerx + 24, self.rect.centery + 20, 'enemy3')
                    projectiles.append(projectile)
        elif self.style == 4:
            if self.hp > 3000:
                if random.randint(1, self.shoot_ratio) == 1:
                    self.data.SFX['ball'].play()
                    projectile = Projectile(self.rect.centerx, self.rect.centery + 100, 'enemy-ball')
                    projectiles.append(projectile)
                elif random.randint(1, self.shoot_ratio) == 1:
                    self.data.SFX['laser-enemy'].play()
                    projectile = Projectile(self.rect.centerx - 155, self.rect.centery, 'enemy-smallball')
                    projectiles.append(projectile)
                    projectile = Projectile(self.rect.centerx + 155, self.rect.centery, 'enemy-smallball')
                    projectiles.append(projectile)
                elif random.randint(1, self.shoot_ratio) == 1:
                    self.data.SFX['laser-enemy'].play()
                    projectile = Projectile(self.rect.centerx - 115, self.rect.centery + 145, 'enemy4')
                    projectiles.append(projectile)
                    projectile = Projectile(self.rect.centerx + 115, self.rect.centery + 145, 'enemy4')
                    projectiles.append(projectile)
                elif random.randint(1, self.shoot_ratio) == 1:
                    self.data.SFX['laser-enemy'].play()
                    projectile = Projectile(self.rect.centerx - 120, self.rect.centery - 105, 'enemy4')
                    projectiles.append(projectile)
                    projectile = Projectile(self.rect.centerx + 120, self.rect.centery - 105, 'enemy4')
                    projectiles.append(projectile)
            else:
                projectiles = self.__boss_berserker(dt)

        return projectiles

    def __boss_berserker(self, dt):
        """Boss sequence in berserker mode"""
        if not self.played_berserker_sound:
            self.data.SFX['enemy-berserker'].play()
            self.data.SFX['enemy-berserker2'].play()
            self.timer = 0
            self.timer2 = 0
            self.played_berserker_sound = True

        self.timer += dt
        self.timer2 += dt
        self.speed = 0.4
        projectiles = []

        if 2000 < self.timer < 8000:
            if self.timer2 > 600:
                self.timer2 = 0
                self.data.SFX['ball'].play()
                projectile = Projectile(self.rect.centerx, self.rect.centery + 100, 'enemy-ball')
                projectiles.append(projectile)
        elif 8500 < self.timer < 15000:
            if self.timer2 > 400:
                self.timer2 = 0
                self.data.SFX['laser-enemy'].play()
                projectile = Projectile(self.rect.centerx - 155, self.rect.centery, 'enemy-smallball')
                projectiles.append(projectile)
                projectile = Projectile(self.rect.centerx + 155, self.rect.centery, 'enemy-smallball')
                projectiles.append(projectile)
        elif 16000 < self.timer < 30000:
            if self.timer2 < 1000:
                self.data.SFX['laser-enemy'].play()
                projectile = Projectile(self.rect.centerx - 120, self.rect.centery - 105, 'enemy4')
                projectiles.append(projectile)
                projectile = Projectile(self.rect.centerx + 120, self.rect.centery - 105, 'enemy4')
                projectiles.append(projectile)
            elif self.timer2 > 2000:
                self.timer2 = 0
        elif self.timer > 30000:
            self.timer = 0

        return projectiles
