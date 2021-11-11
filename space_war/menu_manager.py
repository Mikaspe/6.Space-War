from abc import ABC, abstractmethod

import pygame


class MenuManager(ABC):
    """MenuManager is a superclass for states which use menu navigation."""
    def __init__(self, frame_width: int = 242, xpos_menu_offset: int = 0) -> None:
        """
        Parameters:
            frame_width: width of the menu frame(default=242)
            xpos_menu_offset: offset for items position in the frame menu(default=0 -> text is centered)
        """

        self.num_of_options = len(self.options)
        self.current_menu_pos = self.menu_pos_memory = 0
        self.frame_rect = pygame.Rect((0, 0), (frame_width, self.num_of_options*51))  # Rectangular coordinates of frame
        self.frame_rect.center = self.data.SCREEN_RECT.center
        font_size = 39
        font = pygame.font.Font('freesansbold.ttf', font_size)
        self.lst_text_normal = []
        self.lst_text_highlighted = []
        self.lst_text_rect = []
        self.y_offset = 2/3 * font_size
        for option in self.options:  # Rendering options and storing them in lists
            text_normal = font.render(option, True, (200, 200, 200))
            self.lst_text_normal.append(text_normal)
            self.lst_text_highlighted.append(font.render(option, True, (100, 200, 200)))
            rect = text_normal.get_rect(center=self.frame_rect.midtop)
            rect.x += xpos_menu_offset
            rect.y += self.y_offset
            self.lst_text_rect.append(rect)  # Rectangular coordinates of each option
            self.y_offset += 1/self.num_of_options * self.frame_rect.h

        self.click = False

    @property
    @abstractmethod
    def options(self):
        pass

    @property
    @abstractmethod
    def next_list(self):
        pass

    def cleanup(self) -> None:
        pass

    def startup_menu(self,  initial_menu_pos: int = 0) -> None:
        """Updates initial menu position and resets 'click' flag.
        Called in 'startup' method in a subclass object.

        Parameters:
            initial_menu_pos: Initial menu highlighted option in menu(default=0 -> first option)
        """
        self.current_menu_pos = initial_menu_pos
        self.click = False

    def get_event_menu(self, event: pygame.event) -> None:
        """Menu event handling
        Called in 'get_event' method in a subclass objects.

        Parameters:
            event: PyGame events
        """
        self.click = False  # Resets click flag

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.click = True
            if event.key == pygame.K_DOWN:
                self.current_menu_pos += 1
                if self.current_menu_pos == self.num_of_options:
                    self.current_menu_pos = 0
            if event.key == pygame.K_UP:
                self.current_menu_pos -= 1
                if self.current_menu_pos == -1:
                    self.current_menu_pos = self.num_of_options-1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = True

    def update_menu(self) -> None:
        """Menu navigation.
        Called in 'update' method in a subclass objects.
        """
        mx, my = pygame.mouse.get_pos()

        for option_pos in range(self.num_of_options):  # Mouse menu navigation
            if self.lst_text_rect[option_pos].collidepoint((mx, my)):  # Colission between mouse pointer and menu option
                self.current_menu_pos = option_pos
            if self.current_menu_pos == option_pos:
                if self.click:  # Click by mouse or Enter
                    if self.next_list[option_pos] == 'quit':  # Quit and close window
                        self.quit = True
                    else:  # Menu option selected
                        self.next = self.next_list[option_pos]
                        self.done = True
                        self.data.SFX['menu-select'].play()

        if self.current_menu_pos != self.menu_pos_memory:  # Change position sound
            self.menu_pos_memory = self.current_menu_pos
            self.data.SFX['menu-switch'].play()

    def draw_menu(self) -> None:
        """Draws menu frame and options.
        Called in 'update_menu' method.
        """
        pygame.draw.rect(self.data.SCREEN, (200, 200, 200), self.frame_rect, 5)
        for option_pos in range(self.num_of_options):
            if self.current_menu_pos == option_pos:
                self.data.SCREEN.blit(self.lst_text_highlighted[option_pos], self.lst_text_rect[option_pos])
            else:
                self.data.SCREEN.blit(self.lst_text_normal[option_pos], self.lst_text_rect[option_pos])



