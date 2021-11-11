import pygame

from state import State


class LevelStart(State):
    """Display level text and play sound effect before each level"""
    def __init__(self, data) -> None:
        """
        Parameters:
            data: 'ShareData' object
        """
        self.data = data
        State.__init__(self)
        self.next = 'game'

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """Plays appropriate sound and prepare state depending on level.
        Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        if self.data.level < 8:
            self.data.SFX['start'].play()
            self.sound_length_ms = self.data.SFX['start'].get_length() * 1000
        elif self.data.level == 8:
            self.data.SFX['start_monster'].play()
            self.sound_length_ms = self.data.SFX['start_monster'].get_length() * 1000

        self.text_title = self.data.FONT.render(f'Level {self.data.level}', False, (255, 255, 255))
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
        self.timer += dt
        if self.timer >= self.sound_length_ms:  # State is done when sound effect ends
            self.done = True

    def draw(self,  dt: int) -> None:
        """Draws game background and level text.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            dt: delta time in ms
        """
        self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))
        self.data.SCREEN.blit(self.text_title, self.text_title_rect)
