import os
import sys
import pygame

from CONST import *
from player import Player
from enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        self.load_textures()
        self.load_sounds()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # Initialize a window or screen for display => surface
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)  # pygame object for representing images => Surface
        self.clock = pygame.time.Clock()  # Create an object(Clock type) to help track time
        self.dt = 1

        self.game()

    def load_textures(self):
        self.textures = {}
        for img in os.listdir('img'):  # Return a list containing the names of the files in the directory
            self.textures[img.replace('.png', '')] = pygame.image.load('img/' + img)  # => surface

    def load_sounds(self):
        self.sounds = {}
        for sound in os.listdir('sounds'):  # Return a list containing the names of the files in the directory
            self.sounds[sound.replace('.wav', '')] = pygame.mixer.Sound('sounds/' + sound)  # => sound

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.ENEMYMOVE:
                pass

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.x += round(PLAYER_SPEED * self.dt)
        if keys[pygame.K_LEFT]:
            self.player.x -= round(PLAYER_SPEED * self.dt)
        if keys[pygame.K_SPACE]:
            pass

    def close(self):
        pygame.quit()
        sys.exit(0)

    def game(self):
        self.ENEMYMOVE = pygame.USEREVENT  # Eventy własne
        pygame.time.set_timer(self.ENEMYMOVE, MOVE_RATIO)

        self.enemies = []
        for y in range(3):
            for x in range(int((DRAW_SCREEN_SIZE[0] - BORDER*2) / 37)):
                enemy = Enemy(x*40, y*40, 1)
                self.enemies.append(enemy)

        self.player = Player()

        while True:
            self.check_keys()
            self.check_events()
            self.draw()
            self.refresh_screen()

    def draw(self):
        self.draw_screen.blit(self.textures['background'], (0, 0))
        self.draw_screen.blit(self.textures['player'], self.player)
        for enemy in self.enemies:
            self.draw_screen.blit(self.textures['enemy' + enemy.type], enemy)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)  # Resize to new resolution
        self.screen.blit(scaled, (0, 0))  # Draw one image onto another
        pygame.display.update()  # Update portions of the screen for software displays
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000


Game()
