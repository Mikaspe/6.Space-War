import pygame

from state import State
from menu_manager import MenuManager


class MainMenu(State, MenuManager):
    """Game main menu"""
    def __init__(self, data) -> None:
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, ['Start', 'Spaceship', 'Exit'])

        self.next_list = ['start', 'spaceshipsmenu', 'quit']

    def cleanup(self) -> None:  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self) -> None:  # Wywołane raz na początku tego stanu
        self.data.level = 1
        self.data.gunfire_upgrade = self.data.hp_upgrade = self.data.speed_upgrade = 0
        self.startup_menu()

    def get_event(self, event: pygame.event) -> None:  # Zbiera eventy z control i reaguje na nie w swoj sposob
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True

        self.get_event_menu(event)

    def update(self, keys: pygame.key, dt: int) -> None:  # Updatuje to co sie dzieje w tym stanie
        self.__draw()
        self.update_menu()

    def __draw(self) -> None:  # Rysowanie
        self.data.SCREEN.blit(self.data.GFX[f'background1'], (0, 0))
