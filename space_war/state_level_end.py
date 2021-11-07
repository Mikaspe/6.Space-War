import pygame

from state import State


class LevelEnd(State):
    def __init__(self, data) -> None:  # !!!!!!!!!!!!!!! tutaj typ data
        State.__init__(self)
        self.data = data

    def cleanup(self) -> None:  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self) -> None:  # Wywołane raz na początku tego stanu

        if self.data.hp <= 0:
            self.data.SFX['game-over'].play()
            self.sound_length_ms = self.data.SFX['game-over'].get_length() * 1000
            text = 'TRY AGAIN'
            self.next = 'game'
        elif self.data.level == 8:
            self.data.SFX['killed-monster'].play()
            self.sound_length_ms = self.data.SFX['killed-monster'].get_length() * 1000
            text = 'YOU WIN'
            self.next = 'mainmenu'
        else:
            self.data.SFX['win'].play()
            self.sound_length_ms = self.data.SFX['win'].get_length() * 1000
            text = 'LEVEL COMPLETED'
            self.data.level += 1
            self.next = 'upgrade'

        self.text_title = self.data.FONT.render(text, False, (255, 255, 255))
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
        self.data.SCREEN.blit(self.text_title, self.text_title_rect)