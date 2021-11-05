import sys
import os

import pygame
import pickle

from state_mainmenu import MainMenu
from state_game import Game
from state_start import Start
from state_end import End
from state_pause import Pause
from state_upgrade import Upgrade
from state_spaceshipsmenu import Spaceshipsmenu


class Control:
    """Control and switch between game states."""
    def __init__(self, start_state):
        self.done = False  # When True game closes
        self.clock = pygame.time.Clock()

        self.data = ShareData()
        # All game states
        self.state_dict = {
            'mainmenu': MainMenu(self.data),
            'start': Start(self.data),
            'game': Game(self.data),
            'pause': Pause(self.data),
            'end': End(self.data),
            'upgrade': Upgrade(self.data),
            'spaceshipsmenu': Spaceshipsmenu(self.data)
        }

        self.state_name = start_state  # Name of current state
        self.state = self.state_dict[self.state_name]  # Instance of current state

    def flip_state(self):  # Przerzuca stan z poprzedniego na kolejny
        """Change current state to another."""
        self.state.done = False  # Resetuje flage ktora sprawiła wywołanie flipa
        previous, self.state_name = self.state_name, self.state.next  # Podmiana starego stanu na nowy
        self.state.cleanup()  # Czyści poprzedni stan
        self.state = self.state_dict[self.state_name]  # Podmienia aktualny stan na nowy
        self.state.previous = previous  # Podmienia self.previous
        self.state.startup()  # Uruchamia nowy stan, jego startup

    def update(self, dt):  # W petli. Słuzy do updatowania samego controla jak i aktualnego stanu
        """Updates 'Control' and current state"""
        keys = pygame.key.get_pressed()
        if self.state.quit:  # Jezeli atrybut quit aktualnego stanu jest True to self.done Controla to True wiec wychodzi z pelti i wyłącza gre
            self.done = True
        elif self.state.done:  # Jeżeli atrybut done aktualnego stanu jest True to Control przerzuca stan na kolejny
            self.flip_state()
        self.state.update(keys, dt)  # Wywołanie update stanu, gdzie odbywa się rozgrywka i rysowanie

    def event_loop(self):  # W petli
        """Checks events and send events to the current state"""
        for event in pygame.event.get():  # Sprawdza eventy
            if event.type == pygame.QUIT:
                self.done = True  # Wyłącza gre, bo wychodzi z main_game_loop
            self.state.get_event(event)  # Przesyła do aktualnego stanu, np. Game() wszystkie eventy

    def main_game_loop(self):
        # Gra sie wylaczy gdy self.done = True. Czyli w event loop gdy QUIT lub w update gdy self.state.quit
        # (nie mylic z self.done stanow, ktore koncza stan)
        while not self.done:
            delta_time = self.clock.tick(self.data.FRAMERATE)
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()


class ShareData:
    def __init__(self):
        self.WIN_SIZE = (1024, 768)
        self.FRAMERATE = 80
        self.SCREEN = pygame.display.set_mode(self.WIN_SIZE)
        pygame.display.set_caption('Space-War')
        self.SCREEN_RECT = self.SCREEN.get_rect()
        self.MOVE_RATIO = 30
        self.BORDER = 60
        # self.START_TIME = 140  # Time of 'intro' before each level
        # self.START_BOSS = 350  # Time of 'intro' before boss level
        self.END_TIME = 180  # Time of 'outro' after each level
        pygame.init()  ## !! TUTAJ !?
        self.FONT = pygame.font.Font('../resources/fonts/OpenSans-Bold.ttf', 100)
        self.menu_frame_width = 150*1.61

        self.__GFX = {}
        self.__SFX = {}
        pygame.init()  # OGARNĄĆ TO !!!!!!!!
        pygame.mixer.set_num_channels(50)
        # Dictionary where key is a game level, values are tuples with parameters(x, y, style)
        # used for creating each 'Enemy' spaceship object
        self.__enemies_args = {}

        self.__load_images()
        self.__load_sounds()
        self.__load_level_enemies()

        self.level = 8
        self.max_level = 8
        self.hp = None
        self.gunfire_upgrade = 0
        self.hp_upgrade = 0
        self.speed_upgrade = 0
        self.player_spaceship_style = 'player1'

    @property
    def GFX(self):
        return self.__GFX

    @property
    def SFX(self):
        return self.__SFX

    @property
    def enemies_args(self):
        return self.__enemies_args

    def __load_images(self) -> None:
        """Loads images"""
        print(os.listdir())
        for img in os.listdir('../resources/img/Other'):
            if img.endswith('.png'):
                self.__GFX[img.replace('.png', '')] = pygame.image.load(
                    f'../resources/img/Other/{img}')  # => surface
        for img in os.listdir('../resources/img/Background'):
            self.__GFX[img.replace('.png', '')] = pygame.image.load(
                f'../resources/img/background/{img}')  # => surface
        for img in os.listdir('../resources/img/player'):
            self.__GFX[img.replace('.png', '')] = pygame.image.load(
                f'../resources/img/player/{img}')  # => surface

    def __load_sounds(self) -> None:
        """Loads sounds"""
        for sound in os.listdir('../resources/sounds'):
            self.__SFX[sound.replace('.wav', '')] = pygame.mixer.Sound(f'../resources/sounds/{sound}')  # => sound

    def __load_level_enemies(self) -> None:
        """Loads level enemies from pickle file"""
        with open('game_levels.pickle', 'rb') as handle:
            self.__enemies_args = pickle.load(handle)


pygame.init()
app = Control('mainmenu')  # Sets the initial state of the program
app.main_game_loop()
pygame.quit()
sys.exit()
