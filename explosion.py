import os
import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False

        for animation in os.listdir('animations'):  # Return a list containing the names of the files in the directory
            for frame in os.listdir('animations/' + animation):
                self.sprites.append(pygame.image.load('animations/' + animation + '/' + frame))  # => surface

        self.current_sprite = 4
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def animate(self):
        self.is_animating = True


    def update(self, speed):
        if self.is_animating:
            self.image = self.sprites[int(self.current_sprite)]
            self.current_sprite += speed  # Here is possible to change speed of animation, ex. += 0.5

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False


