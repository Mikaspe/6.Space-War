import pygame


class Explosion(pygame.sprite.Sprite):
    """Explosion animation used when enemy spaceship is destroyed"""
    def __init__(self, data, pos_x: int, pos_y: int) -> None:
        """
        Parameters:
            data: 'ShareData' object
            pos_x: x position where explosion animation will apear
            pos_y: y position where explosion animation will apear
        """
        super().__init__()

        self.sprites = data.GFX['explosion']  # List with all animation frame images
        self.is_animating = False  # Flag which allows updates of animation image when True
        self.current_sprite = 4  # Initial animation frame number
        self.image = self.sprites[self.current_sprite]  # Initial animation frame image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))  # Rectangular coordinates of animation image

    def update(self, speed_of_animation: float = 1) -> None:
        """Updates current explosion frame. Each call updates 'self.image' sprite with next frame image.
        Called in 'draw_game' method in the 'state_game' module.

        Parameters:
            speed_of_animation: Speed of changing frames(default=1). For example if speed_of_animation=0.5 frame
                                changes after 2 calls. If speed_of_animation>1 some of frames'll be skipped.
        """
        self.image = self.sprites[int(self.current_sprite)]
        self.current_sprite += speed_of_animation

        if self.current_sprite >= len(self.sprites):
            # Removes the Sprite from '__animations' sprites group in the 'state_game' module, so it's not more update
            self.kill()
