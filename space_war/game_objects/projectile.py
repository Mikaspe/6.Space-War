import pygame


class Projectile(pygame.sprite.Sprite):
    """Projectile object shot by player or enemy."""
    def __init__(self, data, pos_x: int, pos_y: int, style: str, base_projectile_speed: float = 0.4) -> None:
        """
        Parameters:
            data: 'ShareData' object
            pos_x: x position where projectile will apear
            pos_y: y position where projectile will apear
            style: projectile type
        """
        
        super().__init__()

        self.style = style
        self.__base_projectile_speed = base_projectile_speed

        self.image = data.GFX[f'projectile-{self.style}']
        self.mask = pygame.mask.from_surface(self.image)  # Useful for fast pixel perfect collision detection
        self.rect = self.image.get_rect(center=(pos_x, pos_y))  # Rectangular coordinates of projectile

    def update(self, dt: int) -> None:
        """Moving projectile with defined speed.
        Called in 'update' method in the 'Game' object('state_game' module) or in 'Player' object('player' module)

        Parameters:
            dt: delta time in ms
        """
        speed_x_ratio = 0.3
        if self.style == 'player':
            self.rect.y -= self.__base_projectile_speed * dt
        elif self.style == 'player-l':
            self.rect.y -= self.__base_projectile_speed * dt
            self.rect.x -= round(self.__base_projectile_speed * speed_x_ratio * dt)
        elif self.style == 'player-r':
            self.rect.y -= self.__base_projectile_speed * dt
            self.rect.x += round(self.__base_projectile_speed * speed_x_ratio * dt)
        elif self.style == 'enemy1':
            self.rect.y += self.__base_projectile_speed * dt
        elif self.style == 'enemy2':
            self.rect.y += (self.__base_projectile_speed - 0.1) * dt
        elif self.style == 'enemy3':
            self.rect.y += self.__base_projectile_speed * dt
        elif self.style == 'enemy4':
            self.rect.y += self.__base_projectile_speed * dt
        elif self.style == 'enemy-ball':
            self.rect.y += (self.__base_projectile_speed - 0.23) * dt
        elif self.style == 'enemy-smallball':
            self.rect.y += (self.__base_projectile_speed - 0.10) * dt
