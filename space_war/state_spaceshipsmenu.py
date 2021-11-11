import pygame

from state import State
from menu_manager import MenuManager


class Spaceshipsmenu(State, MenuManager):
    """Option in main menu where player can change player spaceship image"""

    def __init__(self, data) -> None:
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, ['Spaceship1', 'Spaceship2', 'Spaceship3'])
        self.next_list = ['Spaceship1', 'Spaceship2', 'Spaceship3']

        # Title
        font = pygame.font.Font('freesansbold.ttf', 40)
        self.text_spaceship = font.render('Choose spaceship:', True, (200, 200, 200))
        self.text_rect = self.text_spaceship.get_rect()
        self.text_rect.center = self.data.WIN_SIZE[0]/2, self.data.WIN_SIZE[1]/2 - 60

        # Spaceships
        self.spacehip1_rect = self.data.GFX['player1-choosen'].get_rect()
        self.spacehip1_rect.x = self.data.WIN_SIZE[0]/2 - 50
        self.spacehip1_rect.y = self.data.WIN_SIZE[1]/2

        self.spacehip2_rect = self.data.GFX['player2-choosen'].get_rect()
        self.spacehip2_rect.x = self.data.WIN_SIZE[0]/2 - 200
        self.spacehip2_rect.y = self.data.WIN_SIZE[1]/2

        self.spacehip3_rect = self.data.GFX['player3-choosen'].get_rect()
        self.spacehip3_rect.x = self.data.WIN_SIZE[0]/2 + 100
        self.spacehip3_rect.y = self.data.WIN_SIZE[1]/2

        self.lst_text_rect = [self.spacehip1_rect, self.spacehip2_rect, self.spacehip3_rect]

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """State objects preparing. Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        # Initial menu position is the last that player has chosen
        self.startup_menu(initial_menu_pos=int(self.data.player_spaceship_style[-1])-1)

    def get_event(self, event: pygame.event) -> None:
        """Events handling passed as argument by 'Control' object.
        Called in the '__event_loop' method in 'Control' object('control' module).

        Parameters:
            event: PyGame events
        """
        self.click = False  # Resets click flag

        # Menu navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter button
                self.click = True
            if event.key == pygame.K_LEFT:
                self.current_menu_pos += 1
                if self.current_menu_pos == self.num_of_options:
                    self.current_menu_pos = 0
            if event.key == pygame.K_RIGHT:
                self.current_menu_pos -= 1
                if self.current_menu_pos == -1:
                    self.current_menu_pos = self.num_of_options - 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = True

    def update(self, keys: pygame.key, dt: int) -> None:
        """Main processing of the state.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            keys: state of all keyboard buttons
            dt: delta time in ms
        """
        self.update_menu()
        if self.next == 'Spaceship1':
            self.data.player_spaceship_style = 'player1'
        elif self.next == 'Spaceship2':
            self.data.player_spaceship_style = 'player2'
        elif self.next == 'Spaceship3':
            self.data.player_spaceship_style = 'player3'
        self.next = 'mainmenu'

    def draw(self,  dt: int) -> None:
        """Draws background and title on the screen.
        Called in the update method.

        Parameters:
            dt: delta time in ms
        """
        self.data.SCREEN.blit(self.data.GFX[f'background1'], (0, 0))
        self.data.SCREEN.blit(self.text_spaceship, self.text_rect)
        self.draw_menu()

    def draw_menu(self) -> None:
        """Called in 'draw' method. Overrides method in 'MenuManager' superclass.
        Draws spaceship image options.
        """

        for option_pos in range(self.num_of_options):
            if self.current_menu_pos == option_pos:
                self.data.SCREEN.blit(self.data.GFX[f'player{option_pos+1}-choosen'], eval(f'self.spacehip{option_pos+1}_rect'))
            else:
                self.data.SCREEN.blit(self.data.GFX[f'player{option_pos+1}-stop'], eval(f'self.spacehip{option_pos+1}_rect'))
