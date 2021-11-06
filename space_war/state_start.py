import pygame

from state import State


class Start(State):
    def __init__(self, data) -> None:
        self.data = data
        State.__init__(self)
        self.next = 'game'

    def cleanup(self) -> None:  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self) -> None:  # Wywołane raz na początku tego stanu
        if self.data.level < 8:
            self.data.SFX['start'].play()
            self.sound_length_ms = self.data.SFX['start'].get_length() * 1000
        elif self.data.level == 8:
            self.data.SFX['start_monster'].play()
            self.sound_length_ms = self.data.SFX['start_monster'].get_length() * 1000

        self.text_title = self.data.FONT.render(f'Level {self.data.level}', False, (255, 255, 255))
        self.text_title_rect = self.text_title.get_rect(center=self.data.SCREEN_RECT.center)
        self.timer = 0

    def get_event(self, event: pygame.event) -> None:  # Zbiera eventy z control i reaguje na nie w swoj sposob
        pass

    def update(self, keys: pygame.key, dt: int) -> None:  # Updatuje to co sie dzieje w tym stanie
        self.__draw()

        self.timer += dt
        if self.timer >= self.sound_length_ms:
            self.done = True

    def __draw(self) -> None:  # Rysowanie
        self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))
        self.data.SCREEN.blit(self.text_title, self.text_title_rect)
