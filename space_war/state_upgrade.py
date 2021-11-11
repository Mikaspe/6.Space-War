import pygame

from state import State
from menu_manager import MenuManager


class Upgrade(State, MenuManager):
    """Upgrade menu is displayed after finishing each level.
    Player can upgrade one of the abilities(gunfire, health or speed). Maximum upgrade points of one ability is 3."""
    def __init__(self, data) -> None:
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, ['GUNFIRE', 'HEALTH', 'SPEED'], frame_width=290, xpos_menu_offset=-50)
        self.next_list = ['gunfire_upg', 'health_upg', 'speed_upg']
        self.initial_menu_pos = 0

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """State objects preparing. Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        self.startup_menu(initial_menu_pos=self.initial_menu_pos)


    def get_event(self, event: pygame.event) -> None:
        """Events handling passed as argument by 'Control' object.
        Called in the '__event_loop' method in 'Control' object('control' module).

        Parameters:
            event: PyGame events
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Quit and close a window
                self.quit = True

        self.get_event_menu(event)

    def update(self, keys: pygame.key, dt: int) -> None:
        """Main processing of the state.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            keys: state of all keyboard buttons
            dt: delta time in ms
        """
        self.__draw()
        self.update_menu()
        if self.done:  # Player has choosen upgrade
            self.initial_menu_pos = 0
            if self.next == 'gunfire_upg':
                if self.data.gunfire_upgrade < 3:
                    self.data.gunfire_upgrade += 1
                    self.next = 'start'
                else:  # Current gunfire upgrade is max, calls again upgrade menu
                    self.next = 'upgrade'
                    self.initial_menu_pos = 0
            elif self.next == 'health_upg':
                if self.data.hp_upgrade < 3:
                    self.data.hp_upgrade += 1
                    self.next = 'start'
                else:  # Current helath upgrade is max, calls again upgrade menu
                    self.next = 'upgrade'
                    self.initial_menu_pos = 1
            elif self.next == 'speed_upg':
                if self.data.speed_upgrade < 3:
                    self.data.speed_upgrade += 1
                    self.next = 'start'
                else:  # Current speed upgrade is max, calls again upgrade menu
                    self.next = 'upgrade'
                    self.initial_menu_pos = 2

    def __draw(self) -> None:
        """Draws background and upgrade points as a rectangles.
        Called in the update method.
        """
        self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))

        self.upgrade_point_rect = pygame.Rect((0, 0), (15, 15*1.61))
        self.upgrade_point_rect.center = (self.frame_rect.centerx + 50, self.lst_text_rect[0].centery)
        self.space_beetwen_points = 20

        i = 0
        for upgrade in (self.data.gunfire_upgrade, self.data.hp_upgrade, self.data.speed_upgrade):
            self.upgrade_point_rect.centery = self.lst_text_rect[i].centery
            i += 1
            for col in range(1, 4):
                self.upgrade_point_rect.x += self.space_beetwen_points
                if col <= upgrade:  # Fill rectangle if upgrade point already reached
                    pygame.draw.rect(self.data.SCREEN, (200, 200, 200), self.upgrade_point_rect)
                else:  # Empty rectangle if upgrade point not reached
                    pygame.draw.rect(self.data.SCREEN, (200, 200, 200), self.upgrade_point_rect, 5)
            else:
                self.upgrade_point_rect.x -= self.space_beetwen_points * 3

