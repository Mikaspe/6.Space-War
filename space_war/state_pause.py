from state import State

class MenuManager():
    def __init__(self):

        self.startup()

    def cleanup(self):  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self):  # Wywołane raz na początku tego stanu
        pass

    def get_event(self, event):  # Zbiera eventy z control i reaguje na nie w swoj sposob
        pass

    def update(self, keys, dt):  # Updatuje to co sie dzieje w tym stanie
        self.draw()

    def draw(self):  # Rysowanie
        pass
