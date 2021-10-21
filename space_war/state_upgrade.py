from state import State


class Upgrade(State):
    """Upgrade menu is displayed after finishing each level.
    Player can upgrade one of the abilities"""
    def __init__(self, data):
        State.__init__(self)
        self.data = data

        self.next = 'start'

    def cleanup(self):  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self):  # Wywołane raz na początku tego stanu
        pass

    def get_event(self, event):  # Zbiera eventy z control i reaguje na nie w swoj sposob
        pass

    def update(self, keys, dt):  # Updatuje to co sie dzieje w tym stanie
        self.draw()

    def draw(self):  # Rysowanie
        self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))
