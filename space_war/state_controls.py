import pygame

from state import State


class Controls(State):
    """Display game controls"""
    def __init__(self, data) -> None:
        """
        Parameters:
            data: 'ShareData' object
        """
        self.data = data
        State.__init__(self)
        self.next = 'mainmenu'

        controls_title_font = pygame.font.Font('../resources/fonts/OpenSans-Bold.ttf', 70)
        self.text_title = controls_title_font.render('Game controls:', False, (255, 255, 255))
        self.text_title_rect = self.text_title.get_rect(center=(self.data.SCREEN_RECT.centerx, 150))

        self.spacebar_rect = self.data.GFX['spacebar'].get_rect(center=(self.data.SCREEN_RECT.centerx - 150, 400))
        self.arrows_rect = self.data.GFX['arrows'].get_rect(center=(self.data.SCREEN_RECT.centerx + 150, 400))

        controls_text_font = pygame.font.Font('../resources/fonts/OpenSans-Bold.ttf', 40)
        self.text_fire = controls_text_font.render('FIRE', False, (255, 255, 255))
        self.text_fire_rect = self.text_fire.get_rect(center=(self.spacebar_rect.centerx, self.spacebar_rect.centery+50))

        self.text_movement = controls_text_font.render('MOVEMENT', False, (255, 255, 255))
        self.text_movement_rect = self.text_movement.get_rect(center=(self.arrows_rect.centerx, self.arrows_rect.centery+50))

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """.
        Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def get_event(self, event: pygame.event) -> None:
        """Events handling passed as argument by 'Control' object.
        Called in the '__event_loop' method in 'Control' object('control' module).

        Parameters:
            event: PyGame events
        """
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, keys: pygame.key, dt: int) -> None:
        """Main processing of the state.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            keys: state of all keyboard buttons
            dt: delta time in ms
        """
    pass

    def draw(self,  dt: int) -> None:
        """Draws game background and level text.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            dt: delta time in ms
        """
        self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))
        self.data.SCREEN.blit(self.text_title, self.text_title_rect)

        self.data.SCREEN.blit(self.data.GFX['spacebar'], self.spacebar_rect)
        self.data.SCREEN.blit(self.data.GFX['arrows'], self.arrows_rect)
        self.data.SCREEN.blit(self.text_fire, self.text_fire_rect)
        self.data.SCREEN.blit(self.text_movement, self.text_movement_rect)

