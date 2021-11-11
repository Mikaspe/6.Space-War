import sys
import os

import pygame
import pickle

from state_mainmenu import MainMenu
from state_game import Game
from state_level_start import LevelStart
from state_level_end import LevelEnd
from state_pause import Pause
from state_upgrade import Upgrade
from state_spaceshipsmenu import Spaceshipsmenu


class Control:
    """Control and switch between game states. One state is active at one time."""
    def __init__(self, start_state: str = 'mainmenu') -> None:
        """
        Parameters:
            start_state: initial state
        """

        self.done = False  # When True, 'Control' object is done and game closes
        self.clock = pygame.time.Clock()

        self.data = ShareData()  # Object with settings and data shared in the project
        # All game states
        self.state_dict = {
            'mainmenu': MainMenu(self.data),
            'start': LevelStart(self.data),
            'game': Game(self.data),
            'pause': Pause(self.data),
            'end': LevelEnd(self.data),
            'upgrade': Upgrade(self.data),
            'spaceshipsmenu': Spaceshipsmenu(self.data)
        }

        self.state_name = start_state  # Name of a current state
        self.state = self.state_dict[self.state_name]  # Instance of a current state

    def main_game_loop(self) -> None:
        """Main game loop. Control all game states and switch between them. Game quits when while loop breaks"""

        while not self.done:
            delta_time = self.clock.tick(self.data.FRAMERATE)
            self.__event_loop()
            self.__update(delta_time)
            pygame.display.update()

    def __event_loop(self) -> None:
        """Checks and passes events to the current state.
        Called in the 'main_game_loop' method.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # True when user clicks close window button
                self.done = True  # Close the game
            self.state.get_event(event)  # Pass event to the current state

    def __update(self, dt: int) -> None:
        """Updates 'Control' object and current state(calls update method in the current state object).
        Called in the 'main_game_loop' method.

            Parameters:
                dt: delta time in ms
        """
        keys = pygame.key.get_pressed()
        if self.state.quit:  # Quits the game when the atribiute self.quit of the current state is True
            self.done = True
        elif self.state.done:  # Flips state when the atribiute self.done of the current state is True
            self.__flip_state()
        self.state.update(keys, dt)  # .update is common and main method of each state
        self.state.draw(dt)

    def __flip_state(self) -> None:
        """Changes current state to the next one.
        Called in '__update' method
        """
        self.state.done = False  # Resets a flag which caused a call of __flip_state
        # Name of current state is now previous, changes current state name to the new one
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()  # Cleans previous state
        self.state = self.state_dict[self.state_name]  # Set current state to the next one
        self.state.previous = previous  # Memory of the previous state name in the new, current state
        self.state.startup()  # Calls startup method in the new current state


class ShareData:
    """Data object with settings and data shared in the project."""
    def __init__(self) -> None:
        self.WIN_SIZE = (1024, 768)
        self.FRAMERATE = 80
        self.SCREEN = pygame.display.set_mode(self.WIN_SIZE)  # Display surface which'll be drawn
        pygame.display.set_caption('Space-War')  # Caption of the window
        self.SCREEN_RECT = self.SCREEN.get_rect()  # Store rectangular coordinates of the SCREEN

        self.FONT = pygame.font.Font('../resources/fonts/OpenSans-Bold.ttf', 100)  # Text font in level start and end
        self.__GFX = {}  # Images and animations
        self.__SFX = {}  # Sounds
        pygame.mixer.set_num_channels(50)  # Number of sound channels

        # Dictionary where key is a game level, values are tuples with parameters(x_pos, y_pos, style) used for
        # creating each 'Enemy' spaceship object
        self.__enemies_args = {}

        self.__load_images()  # Loads images from directory
        self.__load_sounds()  # Loads sound from directory
        self.__load_level_enemies()  # Loads enemie spaceships composition for each level from pickle file

        self.level = 1  # Current game level
        self.max_level = 8
        self.hp = None
        self.player_spaceship_style = 'player1'
        self.gunfire_upgrade = 1
        self.hp_upgrade = 1
        self.speed_upgrade = 1

    @property
    def GFX(self) -> dict:
        return self.__GFX

    @property
    def SFX(self) -> dict:
        return self.__SFX

    @property
    def enemies_args(self) -> dict:
        return self.__enemies_args

    def __load_images(self) -> None:
        """Loads game images and animations from directories.
        Called in the contructor.
        """
        for folder_name in ('Player', 'Enemy', 'Projectile', 'Background', 'Other'):
            for img in os.listdir(f'../resources/img/{folder_name}'):
                if img.startswith(('player', 'enemy', 'projectile')):
                    self.__GFX[img.replace('.png', '')] = pygame.image.load(f'../resources/img/{folder_name}/{img}').convert_alpha()
                else:
                    self.__GFX[img.replace('.png', '')] = pygame.image.load(f'../resources/img/{folder_name}/{img}')

        for animation in os.listdir('../resources/animations'):
            frames = []
            for frame in os.listdir(f'../resources/animations/{animation}'):
                frames.append(pygame.image.load(f'../resources/animations/{animation}/{frame}'))
            self.__GFX[animation.replace('.png', '')] = frames

    def __load_sounds(self) -> None:
        """Loads game sounds from directory
        Called in the contructor.
        """
        for sound in os.listdir('../resources/sounds'):
            self.__SFX[sound.replace('.wav', '')] = pygame.mixer.Sound(f'../resources/sounds/{sound}')

    def __load_level_enemies(self) -> None:
        """Loads enemie spaceship composition for each level from pickle file.
        Called in the contructor.
        """
        with open('game_levels.pickle', 'rb') as handle:
            # Dictionary where key is a game level, values are tuples with enemy parameters(x_pos, y_pos, style)
            self.__enemies_args = pickle.load(handle)


pygame.init()
app = Control()  # Sets the initial state of the program
app.main_game_loop()

pygame.quit()
sys.exit()
