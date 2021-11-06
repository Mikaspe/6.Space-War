import pygame

from state import State
from menu_manager import MenuManager


class Upgrade(State, MenuManager):
    """Upgrade menu is displayed after finishing each level.
    Player can upgrade one of the abilities"""
    def __init__(self, data) -> None:
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, 290, ['GUNFIRE', 'HEALTH', 'SPEED'], xpos_menu_offset=-50)
        self.next_list = ['gunfire_upg', 'health_upg', 'speed_upg']
        self.initial_menu_pos = 0

    def cleanup(self) -> None:  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self) -> None:  # Wywołane raz na początku tego stanu
        self.startup_menu(initial_menu_pos=self.initial_menu_pos)
        self.__draw()

    def get_event(self, event: pygame.event) -> None:  # Zbiera eventy z control i reaguje na nie w swoj sposob
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True

        self.get_event_menu(event)

    def update(self, keys: pygame.key, dt: int) -> None:  # Updatuje to co sie dzieje w tym stanie
        self.update_menu()
        if self.done:
            self.initial_menu_pos = 0
            if self.next == 'gunfire_upg':
                if self.data.gunfire_upgrade < 3:
                    self.data.gunfire_upgrade += 1
                    self.next = 'start'
                else:
                    self.next = 'upgrade'
                    self.initial_menu_pos = 0
            elif self.next == 'health_upg':
                if self.data.hp_upgrade < 3:
                    self.data.hp_upgrade += 1
                    self.next = 'start'
                else:
                    self.next = 'upgrade'
                    self.initial_menu_pos = 1
            elif self.next == 'speed_upg':
                if self.data.speed_upgrade < 3:
                    self.data.speed_upgrade += 1
                    self.next = 'start'
                else:
                    self.next = 'upgrade'
                    self.initial_menu_pos = 2

    def __draw(self) -> None:  # Rysowanie
        self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))

        self.upgrade_point_rect = pygame.Rect((0, 0), (15, 15*1.61))
        self.upgrade_point_rect.center = (self.frame_rect.centerx + 50, self.lst_text_rect[0].centery)
        self.space_beetwen_points = 20

        # !! Być może da się to lepiej zrobić
        i = 0
        for upgrade in (self.data.gunfire_upgrade, self.data.hp_upgrade, self.data.speed_upgrade):
            self.upgrade_point_rect.centery = self.lst_text_rect[i].centery
            i += 1
            for col in range(1, 4):
                self.upgrade_point_rect.x += self.space_beetwen_points
                if col <= upgrade:
                    pygame.draw.rect(self.data.SCREEN, (200, 200, 200), self.upgrade_point_rect)
                else:
                    pygame.draw.rect(self.data.SCREEN, (200, 200, 200), self.upgrade_point_rect, 5)
            else:
                self.upgrade_point_rect.x -= self.space_beetwen_points * 3

