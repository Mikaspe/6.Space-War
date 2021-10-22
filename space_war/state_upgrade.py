import pygame

from state import State
from menu_manager import MenuManager


class Upgrade(State, MenuManager):
    """Upgrade menu is displayed after finishing each level.
    Player can upgrade one of the abilities"""
    def __init__(self, data):
        self.data = data
        State.__init__(self)
        MenuManager.__init__(self, 290, ['GUNFIRE', 'HEALTH', 'SPEED'], -50)
        self.next_list = ['gunfire_upg', 'health_upg', 'speed_upg']

    def cleanup(self):  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup(self):  # Wywołane raz na początku tego stanu
        self.startup_menu()
        self.draw()

    def get_event(self, event):  # Zbiera eventy z control i reaguje na nie w swoj sposob
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True

        self.get_event_menu(event)

    def update(self, keys, dt):  # Updatuje to co sie dzieje w tym stanie
        self.update_menu()
        if self.done == True:
            print(f'Tutaj jestem: {self.next_list}')
            if self.next == 'gunfire_upg':
                self.data.gunfire_upgrade += 1
            elif self.next == 'health_upg':
                self.data.hp_upgrade += 1
            elif self.next == 'speed_upg':
                self.data.speed_upgrade += 1
            self.next = 'start'

    def draw(self):  # Rysowanie
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

