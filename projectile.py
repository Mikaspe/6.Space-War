import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, style):
        super().__init__()

        self.style = style
        self.base_projectile_speed = 15

        self.image = pygame.image.load('img/projectile/projectile-' + self.style + '.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        speed_x_ratio = 0.3
        if self.style == 'player':
            self.rect.y -= self.base_projectile_speed
        elif self.style == 'player-l':
            self.rect.y -= self.base_projectile_speed
            self.rect.x -= self.base_projectile_speed * speed_x_ratio
        elif self.style == 'player-r':
            self.rect.y -= self.base_projectile_speed
            self.rect.x += self.base_projectile_speed * speed_x_ratio
        elif self.style == 'enemy1':
            self.rect.y += self.base_projectile_speed
        elif self.style == 'enemy2':
            self.rect.y += self.base_projectile_speed - 5
        elif self.style == 'enemy3':
            self.rect.y += self.base_projectile_speed
        elif self.style == 'enemy4':
            self.rect.y += self.base_projectile_speed
        elif self.style == 'enemy-ball':
            self.rect.y += self.base_projectile_speed - 10
        elif self.style == 'enemy-smallball':
            self.rect.y += self.base_projectile_speed - 5
