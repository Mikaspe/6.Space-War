import os
import pickle

import pygame


class GameData:
    """Loads and share game data: images, sounds and enemies"""
    def __init__(self) -> None:
        self.__images = {}
        self.__sounds = {}

        # Dictionary where key is a game level, values are tuples with parameters(x, y, style)
        # used for creating each 'Enemy' spaceship object
        self.__enemies_args = {}

        self.__load_images()
        self.__load_sounds()
        self.__load_level_enemies()

    @property
    def textures(self):
        return self.__images

    @property
    def sounds(self):
        return self.__sounds

    @property
    def enemies_args(self):
        return self.__enemies_args

    def __load_images(self) -> None:
        """Loads images"""
        for img in os.listdir('../resources/img/Other'):
            if img.endswith('.png'):
                self.__images[img.replace('.png', '')] = pygame.image.load(f'../resources/img/Other/{img}')  # => surface
        for img in os.listdir('../resources/img/Background'):
            self.__images[img.replace('.png', '')] = pygame.image.load(f'../resources/img/background/{img}')  # => surface

    def __load_sounds(self) -> None:
        """Loads sounds"""
        for sound in os.listdir('../resources/sounds'):
            self.__sounds[sound.replace('.wav', '')] = pygame.mixer.Sound(f'../resources/sounds/{sound}')  # => sound

    def __load_level_enemies(self) -> None:
        """Loads level enemies from pickle file"""
        with open('game_levels.pickle', 'rb') as handle:
            self.__enemies_args = pickle.load(handle)


