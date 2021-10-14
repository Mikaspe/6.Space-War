import os

import pygame


class Explosion(pygame.sprite.Sprite):
    """Explosion animation."""
    def __init__(self, pos_x: int, pos_y: int) -> None:
        super().__init__()

        self.sprites = []
        self.is_animating = False

        for animation in os.listdir('../resources/animations'):
            for frame in os.listdir(f'../resources/animations/{animation}'):
                self.sprites.append(pygame.image.load(f'../resources/animations/{animation}/{frame}'))  # => surface

        self.current_sprite = 4
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def animate(self) -> None:
        """Change flag value which allows updates of animation image.
        Called when enemy spaceship has been destroyed.
        """
        self.is_animating = True

    def update(self, speed_of_animation: float = 1) -> None:
        """Updates current explosion frame. Each call updates 'self.image' with next frame image.
        Called in 'draw_game' method.

        Parameters:
            speed_of_animation: Speed of changing frames(default=1). For example if speed_of_animation=0.5 frame
                                       changes after 2 calls.
        """
        if self.is_animating:
            self.image = self.sprites[int(self.current_sprite)]
            self.current_sprite += speed_of_animation  # Here is possible to change speed of animation, ex. = 0.5

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False


