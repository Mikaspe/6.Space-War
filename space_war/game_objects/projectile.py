import pygame


class Projectile(pygame.sprite.Sprite):
    """Projectile object"""
    def __init__(self, pos_x: int, pos_y: int, style: str) -> None:
        """
        Parameters:
            pos_x: x position where projectile will apear
            pos_y: y position where projectile will apear
            style: projectile type
        """
        
        super().__init__()

        self.style = style
        self.base_projectile_speed = 0.4

        self.image = pygame.image.load(f'../resources/img/projectile/projectile-{self.style}.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self, dt: int) -> None:
        """Moving projectile with defined speed.
        Called in update method in the state_game module.
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
            self.rect.y += (self.base_projectile_speed - 0.1) * dt
        elif self.style == 'enemy3':
            self.rect.y += self.base_projectile_speed * dt
        elif self.style == 'enemy4':
            self.rect.y += self.base_projectile_speed * dt
        elif self.style == 'enemy-ball':
            self.rect.y += (self.base_projectile_speed - 0.23) * dt
        elif self.style == 'enemy-smallball':
            self.rect.y += (self.base_projectile_speed - 0.10) * dt
