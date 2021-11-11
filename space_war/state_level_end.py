import pygame

from state import State


class LevelEnd(State):
    """Display text and play sound effect after each level"""
    def __init__(self, data) -> None:
        State.__init__(self)
        self.data = data

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """Plays appropriate sound and prepare state depending on end type.
        Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
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

    def get_event(self, event: pygame.event) -> None:
        """Events handling passed as argument by 'Control' object.
        Called in the '__event_loop' method in 'Control' object('control' module).

        Parameters:
            event: PyGame events
        """
        pass

    def update(self, keys: pygame.key, dt: int) -> None:
        """Main processing of the state.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            keys: state of all keyboard buttons
            dt: delta time in ms
        """

        self.__draw()
        self.timer += dt
        if self.timer >= self.sound_length_ms:  # State is done when sound effect ends
            self.done = True

    def __draw(self) -> None:
        """Draws end text on the screen.
        Called in update method.
        """
        self.data.SCREEN.blit(self.text_title, self.text_title_rect)