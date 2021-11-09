import pygame

from space_war.game_objects.projectile import Projectile


class Player(pygame.sprite.Sprite):
    """Player spaceship object.
    Called in Game object in 'state_game' module."""
    def __init__(self, data, style: str, hp_base: int = 3, speed_base: float = 0.4) -> None:
        """
        Parameters:
            data: game data object
            style: type of player spaceship('player1', 'player2' or 'player3')
            hp_base: base player health points(default=3)
            speed_base: base speed of moving player spaceship(default=0.4)
        """
        super().__init__()
        self.data = data

        self.style = style
        self.hp_base = hp_base
        self.data.hp = hp_base
        self.speed_base = speed_base
        self.speed = speed_base
        self.direction = 'stop'
        self.weapon_style = 0

        self.projectiles = pygame.sprite.Group()
        self.timer = 0.0  # Used for delay between player projectiles
        self.shoot_delay = None  # Delay between projectiles in ms
        self.add_laser = False  # Allow to shot new projectile when True

        self.image = self.data.GFX[f'{self.style}-{self.direction}']
        self.mask = pygame.mask.from_surface(self.image)  # Useful for fast pixel perfect collision detection
        # Rectangular coordinates of player spaceship
        self.rect = self.image.get_rect(center=(self.data.WIN_SIZE[0]/2, self.data.WIN_SIZE[1]-75))

    def get_event(self, event: pygame.event) -> None:
        pass

    def update(self, keys: pygame.key, dt: int) -> None:
        """Moves player spaceship, generates projectiles, updates image and keeps spaceship model on the screen.
        Called in 'update' method in 'Game' object('state_game' module).
        Parameters:
            dt: delta time in ms
            keys: state of all keyboard buttons
        """
        self.__move(keys, dt)
        self.__projectile_gen(keys, dt)
        self.image = self.data.GFX[f'{self.style}-{self.direction}']  # Updates spaceship image with proper direction
        self.rect.clamp_ip(self.data.SCREEN_RECT)  # Keeps spaceship model on screen when x pos is too low or high

    def __move(self, keys: pygame.key, dt: int):
        """Moving player spaceship in left or right direction(self.direction) with defined speed(self.speed).
        Called in 'update' method.

        Parameters:
            dt: delta time in ms
            keys: state of all keyboard buttons
        """
        if keys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.rect.x += round(self.speed * dt)
        elif keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.rect.x -= round(self.speed * dt)
        else:
            self.direction = 'stop'

    def __projectile_gen(self, keys: pygame.key, dt: int):
        """Generating and updating projectiles. Removing when outside of the screen.
        Called in update method.

        Parameters:
            dt: delta time in ms
            keys: state of all keyboard buttons
        """
        if pygame.time.get_ticks() - self.timer > self.shoot_delay:
            self.add_laser = True  # Flag allow to add new projectile

        if keys[pygame.K_SPACE]:
            if self.add_laser:
                self.add_laser = False
                self.timer = pygame.time.get_ticks()
                self.data.SFX['laser-player'].play()
                projectile = Projectile(self.data, self.rect.centerx, self.rect.top, 'player')
                self.projectiles.add(projectile)
                if self.weapon_style == 1:  # Generating two more projectiles
                    projectile = Projectile(self.data, self.rect.centerx - 5, self.rect.top, 'player-l')
                    self.projectiles.add(projectile)
                    projectile = Projectile(self.data, self.rect.centerx + 4, self.rect.top, 'player-r')
                    self.projectiles.add(projectile)

        for projectile in self.projectiles:
            if projectile.rect.top < 0:  # Removing projectile when outside of the screen
                self.projectiles.remove(projectile)

        self.projectiles.update(dt)  # Moves projectile

    def draw(self) -> None:
        """Draws player spaceship model and projectiles.
        Called in 'draw' method in 'Game' object('state_game' module).
        """
        self.data.SCREEN.blit(self.image, self.rect)
        self.projectiles.draw(self.data.SCREEN)

    def gunfire_update(self) -> None:
        """Updates player shoot ratio and weapon style depending on actual 'gunfire_upgrade' level.
        Called before each game level."""
        if self.data.gunfire_upgrade == 0:
            self.shoot_delay = 500
            self.weapon_style = 0
        elif self.data.gunfire_upgrade == 1:
            self.shoot_delay = 350
            self.weapon_style = 0
        elif self.data.gunfire_upgrade == 2:
            self.shoot_delay = 200
            self.weapon_style = 0
        elif self.data.gunfire_upgrade == 3:
            self.shoot_delay = 350
            self.weapon_style = 1

    def hp_update(self) -> None:
        """Updates player HP.
        Called before each game level."""
        self.data.hp = self.hp_base + self.data.hp_upgrade

    def speed_update(self) -> None:
        """Updates player speed.
        Called before each game level."""
        self.speed = self.speed_base + 0.15*self.data.speed_upgrade

    def reset(self) -> None:
        """Resets all upgrades.
        Called before starting a new game."""
        self.data.gunfire_upgrade = 0
        self.data.hp_upgrade = 0
        self.data.speed_upgrade = 0

    def change_spaceship(self, style: str) -> None:
        """Changes spacheship model.
        Called when player decide to change model in 'Spaceship choose' menu.

        Parameters:
            style: type of player spaceship('player1', 'player2' or 'player3')
        """
        self.style = style
        self.image = self.data.GFX[f'{self.style}-{self.direction}']
        self.mask = pygame.mask.from_surface(self.image)  # Useful for fast pixel perfect collision detection
        # Rectangular coordinates of player spaceship
        self.rect = self.image.get_rect(center=(self.data.WIN_SIZE[0]/2, self.data.WIN_SIZE[1]-75))

