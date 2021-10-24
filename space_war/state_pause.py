import pygame

from state import State
from menu_manager import MenuManager


class Pause(State, MenuManager):
    def __init__(self, data):
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, self.data.menu_frame_width, ['Continue', 'Main menu', 'Exit'])  # Rozmiar okna dać do stałej

        self.next_list = ['game', 'mainmenu', 'quit']

    def cleanup(self):  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self):  # Wywołane raz na początku tego stanu
        self.startup_menu()

    def get_event(self, event):  # Zbiera eventy z control i reaguje na nie w swoj sposob
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next = 'game'
                self.done = True

        self.get_event_menu(event)

    def update(self, keys, dt):  # Updatuje to co sie dzieje w tym stanie
        self.update_menu()

    def draw(self):  # Rysowanie
        pass
