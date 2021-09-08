import os
import sys
import pygame
import random
import operator

from CONST import *
from player import Player
from enemy import Enemy
from projectile import Projectile


class Game:

    def __init__(self):
        pygame.init()

        self.textures = {}  # Textures(png) from img directory
        self.load_textures()
        self.sounds = {}  # Sounds(wav) from sounds directory
        self.load_sounds()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # Initialize a window or screen for display => surface
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)  # pygame object for representing images => surface

        self.clock = pygame.time.Clock()  # Create an object(Clock type) to help track time
        self.dt = 1  # delta time

        self.player = Player()
        self.enemies = []
        self.projectiles = []

        self.ENEMYMOVE = pygame.USEREVENT  # User event
        pygame.time.set_timer(self.ENEMYMOVE, MOVE_RATIO)

        self.font = pygame.font.Font('OpenSans-Bold.ttf', 20)

        self.click = False

        self.game()

    def load_textures(self):
        for img in os.listdir('img'):  # Return a list containing the names of the files in the directory
            self.textures[img.replace('.png', '')] = pygame.image.load('img/' + img)  # => surface

    def load_sounds(self):
        for sound in os.listdir('sounds'):  # Return a list containing the names of the files in the directory
            self.sounds[sound.replace('.wav', '')] = pygame.mixer.Sound('sounds/' + sound)  # => sound

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies:
                    enemy.move()
            if event.type == pygame.KEYUP:
                self.click = False

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.x += round(PLAYER_SPEED * self.dt)
        if keys[pygame.K_LEFT]:
            self.player.x -= round(PLAYER_SPEED * self.dt)
        if keys[pygame.K_SPACE] and not self.click:
            self.sounds['laser'].play()
            self.click = True
            projectile = Projectile(self.player.centerx, self.player.centery, '1')
            self.projectiles.append(projectile)

    def close(self):
        pygame.quit()
        sys.exit(0)

    def game(self):
        for y in range(3):  # Generating enemie spaceships
            for x in range(int((DRAW_SCREEN_SIZE[0] - BORDER*3) / 90)):
                enemy = Enemy(x*100, y*75, 1, 'right')
                self.enemies.append(enemy)

        while True:
            self.check_keys()
            self.check_events()

            self.enemies.sort(key=operator.attrgetter('x'))
            if self.enemies[0].x < BORDER:
                for enemy in self.enemies:
                    enemy.direction = 'right'
            elif self.enemies[-1].x > DRAW_SCREEN_SIZE[0] - BORDER - self.enemies[-1].w:
                for enemy in self.enemies:
                    enemy.direction = 'left'

            for enemy in self.enemies:
               # if enemy.y >= 150: # usunąc?
               #     self.end('GAME OVER')
                if random.randint(1, ENEMY_SHOT_RATIO) == 0:
                    self.sounds['laser'].play()
                    projectile = Projectile(enemy.centerx, enemy.centery, '2')
                    self.projectiles.append(projectile)

            for projectile in self.projectiles:
                projectile.move()
                if projectile.y < 0 or projectile.y > DRAW_SCREEN_SIZE[1]:
                    self.projectiles.remove(projectile)

            for projectile in self.projectiles:  # To da sie zoptymalizowac z tym wyżej
                if projectile.type == '2' and projectile.colliderect(self.player):
                    self.sounds['hit'].play()
                    self.projectiles.remove(projectile)
                  #  self.player.hp -= 1
                elif projectile.type == '1':
                    for enemy in self.enemies:
                        if projectile.colliderect(enemy):
                            self.sounds['hit'].play()
                            self.enemies.remove(enemy)
                            self.projectiles.remove(projectile)
                            break



            if self.player.hp == 0:
                self.end('GAME OVER')

            if len(self.enemies) == 0:
                self.end('YOU WIN')

            self.draw()
            self.refresh_screen()

    def end(self, text):
        surf = self.font.render(text, False, (255, 255, 255))
        rect = surf.get_rect(center=(int(DRAW_SCREEN_SIZE[0]/2), int(DRAW_SCREEN_SIZE[1]/2)))
        self.draw_screen.blit(surf, rect)
        self.refresh_screen()
        timer = END_TIME
        while timer > 0:
            timer -= self.dt
            self.refresh_screen()
        self.close()

    def draw(self):
        self.draw_screen.blit(self.textures['background'], (0, 0))
        self.draw_screen.blit(self.textures['player1'], self.player)
        for enemy in self.enemies:
            self.draw_screen.blit(self.textures['enemy' + enemy.type], enemy)
        for projectile in self.projectiles:
            self.draw_screen.blit(self.textures['projectile' + projectile.type], projectile)

    def refresh_screen(self):
        pygame.draw.line(self.draw_screen, (0, 255, 255), (BORDER/2, 0), (BORDER/2, 1000), BORDER)
        pygame.draw.line(self.draw_screen, (0, 255, 255), (DRAW_SCREEN_SIZE[0] - BORDER/2, 0), (DRAW_SCREEN_SIZE[0] - BORDER/2, 1000), BORDER)
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)  # Resize to new resolution
        self.screen.blit(scaled, (0, 0))  # Draw one image onto another
        pygame.display.update()  # Update portions of the screen for software displays
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000


Game()
