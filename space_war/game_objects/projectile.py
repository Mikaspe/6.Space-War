import pygame


class Projectile(pygame.sprite.Sprite):
    """Projectile object"""
    def __init__(self, pos_x: int, pos_y: int, style: str) -> None:
        super().__init__()

        self.style = style
        self.base_projectile_speed = 0.4

        self.image = pygame.image.load(f'../resources/img/projectile/projectile-{self.style}.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self, dt) -> None:
        """Moving projectile with defined speed.
        Called when pygame event is 'PROJECTILEMOVE'.
        """
        speed_x_ratio = 0.3
        if self.style == 'player':
            self.rect.y -= self.base_projectile_speed * dt
        elif self.style == 'player-l':
            self.rect.y -= self.base_projectile_speed * dt
            self.rect.x -= round(self.base_projectile_speed * speed_x_ratio * dt)
        elif self.style == 'player-r':
            self.rect.y -= self.base_projectile_speed * dt
            self.rect.x += round(self.base_projectile_speed * speed_x_ratio * dt)
        elif self.style == 'enemy1':
            self.rect.y += self.base_projectile_speed * dt
        elif self.style == 'enemy2':
            self.rect.y += (self.base_projectile_speed - 5) * dt
        elif self.style == 'enemy3':
            self.rect.y += self.base_projectile_speed * dt
        elif self.style == 'enemy4':
            self.rect.y += self.base_projectile_speed * dt
        elif self.style == 'enemy-ball':
            self.rect.y += (self.base_projectile_speed - 10) * dt
        elif self.style == 'enemy-smallball':
            self.rect.y += (self.base_projectile_speed - 5) * dt
