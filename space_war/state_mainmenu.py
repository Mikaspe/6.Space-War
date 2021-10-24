import pygame

from state import State
from menu_manager import MenuManager


class MainMenu(State, MenuManager):
    """Upgrade menu is displayed after finishing each level.
    Player can upgrade one of the abilities"""
    def __init__(self, data):
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, self.data.menu_frame_width, ['Start', 'Spaceship', 'Exit'])

        self.next_list = ['start', 'spaceshipsmenu', 'quit']

    def cleanup(self):  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self):  # Wywołane raz na początku tego stanu
        self.startup_menu()

    def get_event(self, event):  # Zbiera eventy z control i reaguje na nie w swoj sposob
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True

        self.get_event_menu(event)

    def update(self, keys, dt):  # Updatuje to co sie dzieje w tym stanie
        self.draw()
        self.update_menu()

    def draw(self):  # Rysowanie
        self.data.SCREEN.blit(self.data.GFX[f'background1'], (0, 0))
        #self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))










