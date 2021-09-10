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
        pygame.mixer.set_num_channels(20)

        self.textures = {}  # Textures(png) from img directory
        self.load_textures()
        self.sounds = {}  # Sounds(wav) from sounds directory
        self.load_sounds()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # Initialize a window or screen for display => surface
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)  # pygame object for representing images => surface

        self.clock = pygame.time.Clock()  # Create an object(Clock type) to help track time
        self.dt = 1  # delta time

        self.player = Player(1, self.textures['player' + '1'].get_rect().size)
        self.enemies = []
        self.projectiles = []

        self.ENEMYMOVE = pygame.USEREVENT  # User event
        pygame.time.set_timer(self.ENEMYMOVE, ENEMY_MOVE_RATIO)

        self.font = pygame.font.Font('OpenSans-Bold.ttf', 20)

        self.click = False

        self.timer = 0
        self.timer2 = 0


        self.game()

    def load_textures(self):
        for img in os.listdir('img'):  # Return a list containing the names of the files in the directory
            self.textures[img.replace('.png', '')] = pygame.image.load('img/' + img)  # => surface

    def load_sounds(self):
        for sound in os.listdir('sounds'):  # Return a list containing the names of the files in the directory
            self.sounds[sound.replace('.wav', '')] = pygame.mixer.Sound('sounds/' + sound)  # => sound

    def game(self):
        enemy_type = 1  # enemy type ZMIENIC !!!!!!!
        for y in range(3):  # Generating enemie spaceships
            for x in range(int((DRAW_SCREEN_SIZE[0] - BORDER*3) / 90)):
                enemy = Enemy(x*100 + BORDER, y*75, enemy_type, self.textures['enemy' + str(enemy_type)].get_rect().size, 'right')
                self.enemies.append(enemy)

        while True:
            self.check_keys()
            self.check_events()

            self.enemies.sort(key=operator.attrgetter('x'))  # Sorting enemies by x position
            if self.enemies[0].x < BORDER:  # Changing move direction when enemie touch border
                for enemy in self.enemies:
                    enemy.direction = 'right'
            elif self.enemies[-1].x > DRAW_SCREEN_SIZE[0] - BORDER - self.enemies[-1].w:
                for enemy in self.enemies:
                    enemy.direction = 'left'

            for enemy in self.enemies:  # Generating enemies projectiles
                if random.randint(1, ENEMY_SHOT_RATIO) == 1:
                    self.sounds['laser'].play()
                    projectile = Projectile(enemy.centerx, enemy.centery, '2')
                    self.projectiles.append(projectile)

            for projectile in self.projectiles:
                projectile.move()
                if projectile.y < 0 or projectile.y > DRAW_SCREEN_SIZE[1]:  # Removing projectiles if outside of screen
                    self.projectiles.remove(projectile)
                elif projectile.type == '2' and projectile.colliderect(self.player):  # Enemy projectile hits player
                    self.sounds['hit'].play()
                    self.projectiles.remove(projectile)
                    self.player.hp -= 1
                elif projectile.type == '1':  # Player projectile hits enemy
                    for enemy in self.enemies:
                        if projectile.colliderect(enemy):
                            self.projectiles.remove(projectile)
                            enemy.hp -= 1
                            if enemy.hp > 0:
                                self.sounds['hit'].play()
                            else:
                                self.sounds['destroyed'].play()
                                self.enemies.remove(enemy)
                            break  # One projectile hit just one enemy(coliderect sometimes detects more collisions)

            if self.player.hp == 1 and played == 0:
                self.sounds['low-hp'].play()
                played = 1

            elif self.player.hp > 1:
                played = 0
            if self.player.hp == 0:
                self.sounds['game-over'].play()
                self.end('GAME OVER')
            elif not self.enemies:
                self.sounds['win'].play()
                self.end('YOU WIN')

            self.draw()
            self.refresh_screen()

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.direction = 'right'
            if self.player.right < DRAW_SCREEN_SIZE[0]:
                self.player.x += round(PLAYER_SPEED * self.dt)
        elif keys[pygame.K_LEFT]:
            self.player.direction = 'left'
            if self.player.left > 0:
                self.player.x -= round(PLAYER_SPEED * self.dt)
        else:
            self.player.direction = 'stop'
        if keys[pygame.K_SPACE] and not self.click:

            #self.click = True
            #projectile = Projectile(self.player.centerx - 3, self.player.top - 18 - 5, '1')
            self.timer += self.dt
            if self.timer > 10:
                self.timer = 0
                self.sounds['laser'].play()
                projectile = Projectile(self.player.centerx - 3, self.player.top - 18 - 5, '1')
                self.projectiles.append(projectile)
        else:
            self.timer = 100
        if keys[pygame.K_ESCAPE]:
            self.close()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies:
                    enemy.move()
            if event.type == pygame.KEYUP:
                self.click = False

    def draw(self):
        self.draw_screen.blit(self.textures['background1'], (0, 0))
        if self.player.direction == 'stop':
            self.draw_screen.blit(self.textures['player1'], self.player)
        elif self.player.direction == 'left':
            self.draw_screen.blit(self.textures['player1-left'], self.player)
        elif self.player.direction == 'right':
            self.draw_screen.blit(self.textures['player1-right'], self.player)

        for enemy in self.enemies:
            self.draw_screen.blit(self.textures['enemy' + enemy.type], enemy)
        for projectile in self.projectiles:
            self.draw_screen.blit(self.textures['projectile' + projectile.type], projectile)
        for heart in range(self.player.hp):
            self.draw_screen.blit(self.textures['heart'], (heart*12-4, 5))

        if self.player.hp == 1:
            if self.timer2 < 20:
                self.draw_screen.blit(self.textures['heart-black'], (-4, 5))
                self.timer2 += self.dt
            else:
                self.draw_screen.blit(self.textures['heart'], (-4, 5))
                self.timer2 += self.dt
                if self.timer2 > 40:
                    self.timer2 = 0

        print(self.timer2)




    def refresh_screen(self):
        #pygame.draw.line(self.draw_screen, (0, 0, 0), (BORDER/2, 0), (BORDER/2, 1000), BORDER)
        #pygame.draw.line(self.draw_screen, (0, 0, 0), (DRAW_SCREEN_SIZE[0] - BORDER/2, 0), (DRAW_SCREEN_SIZE[0] - BORDER/2, 1000), BORDER)
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)  # Resize to new resolution
        self.screen.blit(scaled, (0, 0))  # Draw one image onto another
        pygame.display.update()  # Update portions of the screen for software displays
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

    def end(self, text):
        self.draw()
        surf = self.font.render(text, False, (255, 255, 255))
        rect = surf.get_rect(center=(int(DRAW_SCREEN_SIZE[0]/2), int(DRAW_SCREEN_SIZE[1]/2)))
        self.draw_screen.blit(surf, rect)
        self.refresh_screen()
        timer = END_TIME
        while timer > 0:
            timer -= self.dt
            self.refresh_screen()
        self.close()

    def close(self):
        pygame.quit()
        sys.exit(0)


Game()
