import pygame


class MenuManager:
    def __init__(self, frame_width, options, xpos_menu_offset=0):  # Teoretycznei nie musiz tego wysylac do nadklasy bo to jest nadklasa
        # ale za to jest bardziej jawne
        self.options = options

        self.num_of_options = len(self.options)
        self.current_menu_pos = 0
        self.frame_rect = pygame.Rect((0, 0), (frame_width, self.num_of_options*51))
        self.frame_rect.center = self.data.SCREEN_RECT.center
        font_size = 39
        font = pygame.font.Font('freesansbold.ttf', font_size)
        self.lst_text_normal = []
        self.lst_text_highlighted = []
        self.lst_text_rect = []
        self.y_offset = 2/3 * font_size#1/len(options) * self.frame_rect.h
        for option in self.options:
            text_normal = font.render(option, True, (200, 200, 200))
            self.lst_text_normal.append(text_normal)
            self.lst_text_highlighted.append(font.render(option, True, (100, 200, 200)))
            rect = text_normal.get_rect(center=self.frame_rect.midtop)
            rect.x += xpos_menu_offset
            rect.y += self.y_offset
            self.lst_text_rect.append(rect)
            self.y_offset += 1/self.num_of_options * self.frame_rect.h

    def cleanup(self):  # Wywołane raz przed przejsciem do next stanu
        pass

    def startup_menu(self,  initial_menu_pos=0):  # Wywołane raz na początku tego stanu
        self.current_menu_pos = initial_menu_pos
        self.click = False

    def get_event_menu(self, event):  # Zbiera eventy z control i reaguje na nie w swoj sposob
        self.click = False
        # if event.type == pygame.QUIT:
        #     self.quit = True
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

    def update_menu(self):  # Updatuje to co sie dzieje w tym stanie
        mx, my = pygame.mouse.get_pos()

        for option_pos in range(self.num_of_options):
            if self.lst_text_rect[option_pos].collidepoint((mx, my)):
                self.current_menu_pos = option_pos
            if self.current_menu_pos == option_pos:
                if self.click:
                    if self.next_list[option_pos] == 'quit':  # Last options is always Quit
                        self.quit = True
                    else:
                        self.next = self.next_list[option_pos]
                        self.done = True

        self.draw_menu()

    def draw_menu(self):  # Rysowanie
        pygame.draw.rect(self.data.SCREEN, (200, 200, 200), self.frame_rect, 5)
        for option_pos in range(self.num_of_options):
            if self.current_menu_pos == option_pos:
                self.data.SCREEN.blit(self.lst_text_highlighted[option_pos], self.lst_text_rect[option_pos])
            else:
                self.data.SCREEN.blit(self.lst_text_normal[option_pos], self.lst_text_rect[option_pos])



