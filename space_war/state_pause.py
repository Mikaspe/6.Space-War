import pygame

from state import State
from menu_manager import MenuManager


class Pause(State, MenuManager):
    """Pauses game and displays pause menu"""
    def __init__(self, data) -> None:
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, ['Continue', 'Main menu', 'Exit'])

        self.next_list = ['game', 'mainmenu', 'quit']

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """State objects preparing. Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        self.startup_menu()

    def get_event(self, event: pygame.event) -> None:
        """Events handling passed as argument by 'Control' object.
        Called in the '__event_loop' method in 'Control' object('control' module).

        Parameters:
            event: PyGame events
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Back to playing game
                self.next = 'game'
                self.done = True

        self.get_event_menu(event)

    def update(self, keys: pygame.key, dt: int) -> None:
        """Main processing of the state.

        Parameters:
            keys: state of all keyboard buttons
            dt: delta time in ms
        """
        self.update_menu()

    def __draw(self) -> None:
        pass
