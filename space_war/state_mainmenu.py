import pygame

from .state import State
from .menu_manager import MenuManager


class MainMenu(State, MenuManager):
    """Game main menu."""
    def __init__(self, data) -> None:
        """
        Parameters:
            data: 'ShareData' object
        """
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self)

    @property
    def options(self):
        """Text of menu options. Used in superclass 'MenuManager'"""
        return ['Start', 'Spaceship', 'Controls', 'Exit']

    @property
    def next_list(self):
        """Next states after clicking corresponding menu option."""
        return ['start', 'spaceshipsmenu', 'controls', 'quit']

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """State objects preparing. Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        self.data.level = 1
        self.data.gunfire_upgrade = self.data.hp_upgrade = self.data.speed_upgrade = 0
        self.startup_menu()

    def get_event(self, event: pygame.event) -> None:
        """Events handling passed as argument by 'Control' object.
         Called in the '__event_loop' method in 'Control' object('control' module).

         Parameters:
             event: PyGame events
         """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Quit and close window
                self.quit = True

        self.get_event_menu(event)

    def update(self, keys: pygame.key, dt: int) -> None:
        """Main processing of the state.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            keys: state of all keyboard buttons
            dt: delta time in ms
        """
        self.update_menu()

    def draw(self,  dt: int) -> None:
        """Draws background on the screen.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            dt: delta time in ms
        """
        self.data.SCREEN.blit(self.data.GFX[f'background1'], (0, 0))
        self.draw_menu()
