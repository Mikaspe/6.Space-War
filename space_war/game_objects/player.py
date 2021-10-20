import os

import pygame

from space_war.game_objects.projectile import Projectile


class Player(pygame.sprite.Sprite):
    """Player's spaceship object"""
    def __init__(self, data, style: str, hp_base: int = 3, speed_base: float = 0.5, shoot_ratio: float = 20) -> None:
        super().__init__()
        self.data = data

        self.style = style
        self.hp_base = hp_base
        self.data.hp = hp_base
        self.speed_base = speed_base
        self.speed = speed_base
        self.shoot_ratio = shoot_ratio
        self.direction = 'stop'
        self.weapon_style = 0

        self.projectiles = pygame.sprite.Group()
        self.timer = 0.0
        self.projectile_delay = 500
        self.add_laser = False

        self.textures = {}
        for img in os.listdir('../resources/img/Player'):  # Loading all player spaceships images
            self.textures[img.replace('.png', '')] = pygame.image.load(f'../resources/img/player/{img}').convert_alpha()

        self.image = self.textures[f'{self.style}-{self.direction}']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.data.WIN_SIZE[0]/2, self.data.WIN_SIZE[1]-75))

    def get_event(self, event):
        pass

    def update(self, keys, dt):
        # updates current spaceship image with proper direction(left, right or stop)
        self.image = self.textures[f'{self.style}-{self.direction}']

        if keys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.rect.x += round(self.speed * dt)
        elif keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.rect.x -= round(self.speed * dt)
        else:
            self.direction = 'stop'

        if pygame.time.get_ticks() - self.timer > self.projectile_delay:
            self.add_laser = True

        if keys[pygame.K_SPACE]:
            if self.add_laser:
                self.add_laser = False
                self.timer = pygame.time.get_ticks()
                self.data.SFX['laser-player'].play()
                projectile = Projectile(self.rect.centerx, self.rect.top, 'player')
                self.projectiles.add(projectile)
                if self.weapon_style == 1:
                    projectile = Projectile(self.rect.centerx - 5, self.rect.top, 'player-l')
                    self.projectiles.add(projectile)
                    projectile = Projectile(self.rect.centerx + 4, self.rect.top, 'player-r')
                    self.projectiles.add(projectile)

        for projectile in self.projectiles:
            if projectile.rect.top < 0:
                self.projectiles.remove(projectile)

        self.rect.clamp_ip(self.data.SCREEN_RECT)  # Keep spaceship model on screen when x pos is too low or high
        self.projectiles.update(dt)

    def draw(self):
        self.data.SCREEN.blit(self.image, self.rect)
        self.projectiles.draw(self.data.SCREEN)

    def gunfire_update(self) -> None:
        """Updates player shoot ratio and weapon style depending on actual 'gunfire_upgrade' level.
        Called before each game level."""
        if self.data.gunfire_upgrade == 0:
            self.shoot_ratio = 25
            self.weapon_style = 0
        elif self.data.gunfire_upgrade == 1:
            self.shoot_ratio = 17
            self.weapon_style = 0
        elif self.data.gunfire_upgrade == 2:
            self.shoot_ratio = 10
            self.weapon_style = 0
        elif self.data.gunfire_upgrade == 3:
            self.shoot_ratio = 20
            self.weapon_style = 1

    def hp_update(self) -> None:
        """Updates player HP.
        Called before each game level."""
        self.data.hp = self.hp_base + self.data.hp_upgrade

    def speed_update(self) -> None:
        """Updates player speed.
        Called before each game level."""
        self.speed = self.speed_base + 0.3*self.data.speed_upgrade

    def reset(self) -> None:
        """Resets all upgrades.
        Called before starting a game."""
        self.data.gunfire_upgrade = 0
        self.data.hp_upgrade = 0
        self.data.speed_upgrade = 0

    def change_spaceship(self, style: str) -> None:
        """Changes spacheship model.
        Called when player decide to change model in 'Spaceship choose' menu before game"""
        self.style = style
        self.image = self.textures[f'{self.style}-{self.direction}']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.data.WIN_SIZE[0]/2, self.data.WIN_SIZE[1]-75))

