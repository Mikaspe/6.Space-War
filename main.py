import os
import sys
import pygame
import random
import operator


from CONST import *
from player import Player
from enemy import Enemy
from projectile import Projectile
from explosion import Explosion


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.set_num_channels(30)

        self.textures = {}  # Textures(png) from img directory
        self.load_textures()

        self.sounds = {}  # Sounds(wav) from sounds directory
        self.load_sounds()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # Initialize a window or screen for display => surface
        pygame.display.set_caption('Space-War')
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)  # pygame object for representing images => surface

        self.clock = pygame.time.Clock()  # Create an object(Clock type) to help track time
        self.dt = 1  # delta time

        self.player = Player('player1')
        self.enemies = []
        self.projectiles = []

        self.ENEMYMOVE = pygame.USEREVENT  # User event for moving enemy
        pygame.time.set_timer(self.ENEMYMOVE, ENEMY_MOVE_RATIO)

        self.font = pygame.font.Font('OpenSans-Bold.ttf', 100)

        self.timer = 0
        self.timer2 = 0
        
        self.border = 70

        self.animations = pygame.sprite.Group()

        self.go_to_main_menu = False
        self.level = 1

        self.level_switch()

    def load_textures(self):
        self.textures['heart'] = pygame.image.load('img/heart.png')  # => surface
        self.textures['heart-black'] = pygame.image.load('img/heart-black.png')  # => surface

    def load_sounds(self):
        for sound in os.listdir('sounds'):  # Return a list containing the names of the files in the directory
            self.sounds[sound.replace('.wav', '')] = pygame.mixer.Sound('sounds/' + sound)  # => sound

    def level_switch(self):

        while True:
            self.go_to_main_menu = False
            self.main_menu()
            self.level = 1
            self.player.reset()
            while True:
                self.player.hp_update()
                self.player.speed_update()
                self.player.gunfire_update()
                self.start('Level ' + str(self.level))
                self.game()
                self.projectiles.clear()
                self.animations.empty()
                self.enemies.clear()
                if self.go_to_main_menu:
                    break

    def game(self):

        # Generating enemie spaceships depends on actual level
        if self.level == 1:
            enemy_style = 1
            for y in range(1, 3):
                for x in range(6):
                    enemy = Enemy(x*100 + self.border, y*75, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 2:
            enemy_style = 1
            for y in range(3):
                for x in range(8):
                    enemy = Enemy(x*100 + self.border, y*75, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 3:
            enemy_style = 2
            for y in range(2):
                for x in range(3):
                    enemy = Enemy(x*100 + self.border, y*75, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 4:
            enemy_style = 1
            for y in range(3):
                if y == 2:
                    enemy_style = 2
                for x in range(8):
                    enemy = Enemy(x*100 + self.border, y*75, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 5:
            enemy_style = 3
            for y in range(2):
                for x in range(1, 3):
                    enemy = Enemy(x*100 + self.border, y*75, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 6:
            enemy_style = 3
            for y in range(3):
                if y == 2:
                    enemy_style = 2
                for x in range(6):
                    enemy = Enemy(x*100 + self.border, y*75 + 40, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 7:
            enemy_style = 3
            for y in range(4):
                if y == 1:
                    enemy_style = 1
                elif y == 2:
                    enemy_style = 2
                for x in range(8):
                    enemy = Enemy(x*100 + self.border, y*75 + 40, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 8:
            enemy_style = 4
            self.border = 10
            enemy = Enemy(DRAW_SCREEN_SIZE[0]/2, 170, enemy_style)
            enemy.shoot_ratio = 50
            self.enemies.append(enemy)

        timer = 0
        timer2 = 0
        start_seq = False  # Boss fight(lvl 8) sequence
        play_berserker_sound = True
        play_lowhp_sound = True

        while True:
            self.check_keys()
            self.check_events()

            # Changing enemies move direction when reach self.border
            self.enemies.sort(key=operator.attrgetter('rect.x'))  # Sorting enemies by x position
            if self.enemies[0].rect.x < self.border:  # Left border
                for enemy in self.enemies:
                    enemy.direction = 'right'
            elif self.enemies[-1].rect.x > DRAW_SCREEN_SIZE[0] - self.border - self.enemies[-1].rect.w:  # Right border
                for enemy in self.enemies:
                    enemy.direction = 'left'

            for enemy in self.enemies:  # Generating enemies projectiles

                if enemy.style == 1:
                    if random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser'].play()
                        projectile = Projectile(enemy.rect.centerx, enemy.rect.centery, 'enemy1')
                        self.projectiles.append(projectile)
                elif enemy.style == 2:
                    if random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser'].play()
                        projectile = Projectile(enemy.rect.centerx, enemy.rect.centery, 'enemy2')
                        self.projectiles.append(projectile)
                elif enemy.style == 3:
                    if random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser'].play()
                        projectile = Projectile(enemy.rect.centerx, enemy.rect.centery, 'enemy3')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx - 24, enemy.rect.centery + 20, 'enemy3')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx + 24, enemy.rect.centery + 20, 'enemy3')
                        self.projectiles.append(projectile)
                elif enemy.style == 4:
                    if enemy.hp < 300:
                        start_seq = True
                    elif random.randint(1, enemy.shoot_ratio + 100) == 1:
                        self.sounds['ball'].play()
                        projectile = Projectile(enemy.rect.centerx, enemy.rect.centery + 100, 'enemy-ball')
                        self.projectiles.append(projectile)
                    elif random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser'].play()
                        projectile = Projectile(enemy.rect.centerx - 155, enemy.rect.centery, 'enemy-smallball')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx + 155, enemy.rect.centery, 'enemy-smallball')
                        self.projectiles.append(projectile)
                    elif random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser'].play()
                        projectile = Projectile(enemy.rect.centerx - 115, enemy.rect.centery + 145, 'enemy4')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx + 115, enemy.rect.centery + 145, 'enemy4')
                        self.projectiles.append(projectile)
                    elif random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser'].play()
                        projectile = Projectile(enemy.rect.centerx - 120, enemy.rect.centery - 105, 'enemy4')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx + 120, enemy.rect.centery - 105, 'enemy4')
                        self.projectiles.append(projectile)

                    if start_seq:
                        if play_berserker_sound:
                            self.sounds['enemy-berserker'].play()
                            self.sounds['enemy-berserker2'].play()
                            play_berserker_sound = False

                        timer += self.dt
                        timer2 += self.dt

                        enemy.speed = 12

                        if 200 < timer < 800:
                            if timer2 > 60:
                                timer2 = 0
                                self.sounds['ball'].play()
                                projectile = Projectile(enemy.rect.centerx, enemy.rect.centery + 100, 'enemy-ball')
                                self.projectiles.append(projectile)
                        elif 850 < timer < 1500:
                            if timer2 > 40:
                                timer2 = 0
                                self.sounds['laser'].play()
                                projectile = Projectile(enemy.rect.centerx - 155, enemy.rect.centery, 'enemy-smallball')
                                self.projectiles.append(projectile)
                                projectile = Projectile(enemy.rect.centerx + 155, enemy.rect.centery, 'enemy-smallball')
                                self.projectiles.append(projectile)
                        elif 1600 < timer < 3000:
                            if timer2 < 100:
                                self.sounds['laser'].play()
                                projectile = Projectile(enemy.rect.centerx - 120, enemy.rect.centery - 105, 'enemy4')
                                self.projectiles.append(projectile)
                                projectile = Projectile(enemy.rect.centerx + 120, enemy.rect.centery - 105, 'enemy4')
                                self.projectiles.append(projectile)
                            elif timer2 > 200:
                                timer2 = 0
                        elif timer > 3000:
                            timer = 0

            for projectile in self.projectiles:

                # Removing projectiles if outside of screen
                if projectile.rect.y < 0 or projectile.rect.y > DRAW_SCREEN_SIZE[1]:
                    self.projectiles.remove(projectile)
                # Enemy projectile hits player
                elif projectile.style == 'enemy-ball' and pygame.sprite.collide_mask(self.player, projectile):
                    self.sounds['ball-hit'].play()
                    self.projectiles.remove(projectile)
                    self.player.hp -= 1
                elif projectile.style == 'enemy-smallbal' and pygame.sprite.collide_mask(self.player, projectile):
                    self.sounds['ball-hit'].play()
                    self.projectiles.remove(projectile)
                    self.player.hp -= 1
                elif projectile.style.startswith('enemy') and pygame.sprite.collide_mask(self.player, projectile):
                    self.sounds['hit'].play()
                    self.projectiles.remove(projectile)
                    self.player.hp -= 1

                # Player projectile hits enemy
                elif 'player' in projectile.style:
                    for enemy in self.enemies:
                        if pygame.sprite.collide_mask(enemy, projectile):
                            self.projectiles.remove(projectile)
                            enemy.hp -= 1
                            if enemy.hp > 0:
                                self.sounds['hit'].play()
                            elif enemy.hp == 0:
                                self.sounds['destroyed'].play()
                                self.explosion = Explosion(enemy.rect.x, enemy.rect.y)
                                self.explosion.animate()
                                self.animations.add(self.explosion)
                                self.enemies.remove(enemy)
                                for enemy in self.enemies:  # Speed of enemies increases when number of them decrease
                                    enemy.speed += 0.1
                            break  # One projectile hits just one enemy(.collide_mask sometimes detects more collisions)

            if self.player.hp == 1 and play_lowhp_sound:
                self.sounds['low-hp'].play()
                play_lowhp_sound = False
            elif self.player.hp <= 0:
                self.sounds['game-over'].play()
                self.end('GAME OVER')
                break
            elif self.level == 8 and not self.enemies:
                self.sounds['killed-monster'].play()
                self.end('YOU WIN')
                self.go_to_main_menu = True
                break
            elif not self.enemies:
                self.sounds['win'].play()
                self.end('YOU WIN')
                self.upgrade_menu()
                self.level += 1
                break

            self.draw()
            self.refresh_screen()

    def check_keys(self):
        # Moving and shooting player spaceship
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.direction = 'right'
            if self.player.rect.right < DRAW_SCREEN_SIZE[0]:
                self.player.rect.x += round(self.player.speed * self.dt)
        elif keys[pygame.K_LEFT]:
            self.player.direction = 'left'
            if self.player.rect.left > 0:
                self.player.rect.x -= round(self.player.speed * self.dt)
        else:
            self.player.direction = 'stop'
        if keys[pygame.K_SPACE]:
            self.timer += self.dt
            if self.timer > self.player.shoot_ratio:
                self.sounds['laser'].play()
                projectile = Projectile(self.player.rect.centerx, self.player.rect.top, 'player')
                self.projectiles.append(projectile)
                self.timer = 0
                if self.player.weapon_style == 1:
                    projectile = Projectile(self.player.rect.centerx - 5, self.player.rect.top, 'player-l')
                    self.projectiles.append(projectile)
                    projectile = Projectile(self.player.rect.centerx + 4, self.player.rect.top, 'player-r')
                    self.projectiles.append(projectile)
        else:
            self.timer = 100
        if keys[pygame.K_ESCAPE]:
            self.pause_menu()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies:
                    enemy.move()
                for projectile in self.projectiles:
                    projectile.move()

    def draw(self):

        self.draw_screen.blit(self.textures['background' + str(self.level)], (0, 0))

        self.draw_screen.blit(self.player.get_image(), self.player.rect)

        for sprite in self.animations:
            sprite.update(1.6)

        self.animations.draw(self.draw_screen)

        for enemy in self.enemies:
            self.draw_screen.blit(enemy.image, enemy)
        for projectile in self.projectiles:
            self.draw_screen.blit(projectile.image, projectile)
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

        font = pygame.font.Font('freesansbold.ttf', 15)

        text_level = font.render(str(self.level) + '/8', True, (200, 200, 200))
        text_rect = text_level.get_rect()
        text_rect.right = DRAW_SCREEN_SIZE[0] - 5
        text_rect.y = 8
        self.draw_screen.blit(text_level, text_rect)

    def refresh_screen(self):
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

        if self.level == 8:
            timer = 200

        while timer > 0:
            timer -= self.dt
            self.refresh_screen()

    def close(self):
        pygame.quit()
        sys.exit(0)

    def main_menu(self):

        draw_screen_rect = self.draw_screen.get_rect()
        frame = pygame.Rect((0, 0), (150*1.61, 150))
        frame.center = draw_screen_rect.center

        font = pygame.font.Font('freesansbold.ttf', 40)

        text_start = font.render('Start', True, (200, 200, 200))
        text_start_highlighted = font.render('Start', True, (100, 200, 200))
        text_rect = text_start.get_rect()
        text_rect.center = draw_screen_rect.center
        text_rect.y -= 1/3 * frame.h #+ 100

        text_spaceship = font.render('Spaceship', True, (200, 200, 200))
        text_spaceship_highlighted = font.render('Spaceship', True, (100, 200, 200))
        text2_rect = text_spaceship.get_rect()
        text2_rect.center = draw_screen_rect.center

        text_exit = font.render('Exit', True, (200, 200, 200))
        text_exit_highligted = font.render('Exit', True, (100, 200, 200))
        text3_rect = text_exit.get_rect()
        text3_rect.center = draw_screen_rect.center
        text3_rect.y += 1/3 * frame.h
        menu_pos = 1

        m1 = True
        m2 = True
        m3 = True

        while True:
            self.draw_screen.blit(self.textures['background1'], (0, 0))
            pygame.draw.rect(self.draw_screen, (200, 200, 200), frame, 5)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                    if event.key == pygame.K_RETURN:
                        click = True
                    if event.key == pygame.K_DOWN:
                        menu_pos += 1
                        if menu_pos == 4:
                            menu_pos = 1
                    if event.key == pygame.K_UP:
                        menu_pos -= 1
                        if menu_pos == 0:
                            menu_pos = 3
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            mx, my = pygame.mouse.get_pos()

            if text_rect.collidepoint((mx, my)) and m1:
                menu_pos = 1
                m1 = False
                m2 = True
                m3 = True

            if text2_rect.collidepoint((mx, my)) and m2:
                menu_pos = 2
                m1 = True
                m2 = False
                m3 = True

            if text3_rect.collidepoint((mx, my)) and m3:
                menu_pos = 3
                m1 = True
                m2 = True
                m3 = False

            if menu_pos == 1:
                self.draw_screen.blit(text_start_highlighted, text_rect)
                if click:
                    break
            else:
                self.draw_screen.blit(text_start, text_rect)

            if menu_pos == 2:
                self.draw_screen.blit(text_spaceship_highlighted, text2_rect)
                if click:
                    self.spaceship_choose()
            else:
                self.draw_screen.blit(text_spaceship, text2_rect)

            if menu_pos == 3:
                self.draw_screen.blit(text_exit_highligted, text3_rect)
                if click:
                    self.close()
            else:
                self.draw_screen.blit(text_exit, text3_rect)

            self.refresh_screen()

    def pause_menu(self):
        draw_screen_rect = self.draw_screen.get_rect()
        frame = pygame.Rect((0, 0), (150 * 1.61, 150))
        frame.center = draw_screen_rect.center

        font = pygame.font.Font('freesansbold.ttf', 40)
        text_continue = font.render('Continue', True, (200, 200, 200))
        text_continue_highlighted = font.render('Continue', True, (100, 200, 200))
        text_rect = text_continue.get_rect()
        text_rect.center = draw_screen_rect.center
        text_rect.y -= 1 / 3 * frame.h

        text_main_menu = font.render('Main menu', True, (200, 200, 200))
        text_main_menu_highlighted = font.render('Main menu', True, (100, 200, 200))
        text2_rect = text_main_menu.get_rect()
        text2_rect.center = draw_screen_rect.center

        text_exit = font.render('Exit', True, (200, 200, 200))
        text_exit_highlighted = font.render('Exit', True, (100, 200, 200))
        text3_rect = text_exit.get_rect()
        text3_rect.center = draw_screen_rect.center
        text3_rect.y += 1 / 3 * frame.h

        pygame.draw.rect(self.draw_screen, (200, 200, 200), frame, 5)

        m1 = True
        m2 = True
        m3 = True
        menu_pos = 1
        while True:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                    if event.key == pygame.K_RETURN:
                        click = True
                    if event.key == pygame.K_DOWN:
                        menu_pos += 1
                        if menu_pos == 4:
                            menu_pos = 1
                    if event.key == pygame.K_UP:
                        menu_pos -= 1
                        if menu_pos == 0:
                            menu_pos = 3
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            mx, my = pygame.mouse.get_pos()

            if text_rect.collidepoint((mx, my)) and m1:
                menu_pos = 1
                m1 = False
                m2 = True
                m3 = True

            if text2_rect.collidepoint((mx, my)) and m2:
                menu_pos = 2
                m1 = True
                m2 = False
                m3 = True

            if text3_rect.collidepoint((mx, my)) and m3:
                menu_pos = 3
                m1 = True
                m2 = True
                m3 = False

            if menu_pos == 1:
                self.draw_screen.blit(text_continue_highlighted, text_rect)
                if click:
                    break
            else:
                self.draw_screen.blit(text_continue, text_rect)

            if menu_pos == 2:
                self.draw_screen.blit(text_main_menu_highlighted, text2_rect)
                if click:
                    self.main_menu()
            else:
                self.draw_screen.blit(text_main_menu, text2_rect)

            if menu_pos == 3:
                self.draw_screen.blit(text_exit_highlighted, text3_rect)
                if click:
                    self.close()
            else:
                self.draw_screen.blit(text_exit, text3_rect)

            self.refresh_screen()



    def spaceship_choose(self):

        font = pygame.font.Font('freesansbold.ttf', 40)
        text_spaceship = font.render('Choose spaceship:', True, (200, 200, 200))
        text_rect = text_spaceship.get_rect()
        text_rect.center = DRAW_SCREEN_SIZE[0]/2, DRAW_SCREEN_SIZE[1]/2
        text_rect.y -= 60

        spacehip1_rect = self.textures['player1-choosen'].get_rect()
        spacehip1_rect.x = DRAW_SCREEN_SIZE[0]/2 - 50
        spacehip1_rect.y = DRAW_SCREEN_SIZE[1]/2

        spacehip2_rect = self.textures['player2-choosen'].get_rect()
        spacehip2_rect.x = DRAW_SCREEN_SIZE[0] / 2 - 200
        spacehip2_rect.y = DRAW_SCREEN_SIZE[1] / 2

        spacehip3_rect = self.textures['player3-choosen'].get_rect()
        spacehip3_rect.x = DRAW_SCREEN_SIZE[0] / 2 + 100
        spacehip3_rect.y = DRAW_SCREEN_SIZE[1] / 2

        m1 = True
        m2 = True
        m3 = True
        menu_pos = 1

        while True:
            self.draw_screen.blit(self.textures['background1'], (0, 0))
            self.draw_screen.blit(text_spaceship, text_rect)
            click = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                    if event.key == pygame.K_RETURN:
                        click = True
                    if event.key == pygame.K_LEFT:
                        menu_pos += 1
                        if menu_pos == 4:
                            menu_pos = 1
                    if event.key == pygame.K_RIGHT:
                        menu_pos -= 1
                        if menu_pos == 0:
                            menu_pos = 3
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            mx, my = pygame.mouse.get_pos()

            if spacehip1_rect.collidepoint((mx, my)) and m1:
                menu_pos = 1
                m1 = False
                m2 = True
                m3 = True

            if spacehip2_rect.collidepoint((mx, my)) and m2:
                menu_pos = 2
                m1 = True
                m2 = False
                m3 = True

            if spacehip3_rect.collidepoint((mx, my)) and m3:
                menu_pos = 3
                m1 = True
                m2 = True
                m3 = False

            if menu_pos == 1:
                self.draw_screen.blit(self.textures['player1-choosen'], (spacehip1_rect.x, spacehip1_rect.y))
                if click:
                    self.player.style = 1
                    break
            else:
                self.draw_screen.blit(self.textures['player1-stop'], (spacehip1_rect.x, spacehip1_rect.y))

            if menu_pos == 2:
                self.draw_screen.blit(self.textures['player2-choosen'], (spacehip2_rect.x, spacehip2_rect.y))
                if click:
                    self.player.style = 2
                    break
            else:
                self.draw_screen.blit(self.textures['player2-stop'], (spacehip2_rect.x, spacehip2_rect.y))

            if menu_pos == 3:
                self.draw_screen.blit(self.textures['player3-choosen'], (spacehip3_rect.x, spacehip3_rect.y))
                if click:
                    self.player.style = 3
                    break
            else:
                self.draw_screen.blit(self.textures['player3-stop'], (spacehip3_rect.x, spacehip3_rect.y))

            self.refresh_screen()

    def upgrade_menu(self):
        self.draw_screen.blit(self.textures['background1'], (0, 0))

        font = pygame.font.Font('freesansbold.ttf', 15)

        text_level = font.render(str(self.level) + '/8', True, (200, 200, 200))
        text_rect = text_level.get_rect()
        text_rect.right = DRAW_SCREEN_SIZE[0] - 5
        text_rect.y = 8
        self.draw_screen.blit(text_level, text_rect)

        draw_screen_rect = self.draw_screen.get_rect()
        frame = pygame.Rect((0, 0), (290, 150))
        frame.center = draw_screen_rect.center
        pygame.draw.rect(self.draw_screen, (200, 200, 200), frame, 5)

        font = pygame.font.Font('freesansbold.ttf', 40)

        text_gunfire = font.render('GUNFIRE', True, (200, 200, 200))
        text_gunfire_highlighted = font.render('GUNFIRE', True, (100, 200, 200))
        text_rect = text_gunfire.get_rect()
        text_rect.center = frame.center
        text_rect.x = frame.x + 15
        text_rect.y -= 1/3 * frame.h - 5

        upgrade_point_rect = pygame.Rect((0, 0), (15, 15*1.61))

        upgrade_point_rect.center = text_rect.center
        upgrade_point_rect.x += 100
        upgrade_point_rect.y -= 2

        for col in range(1, 4):
            upgrade_point_rect.x += 20
            if col <= self.player.gunfire_upgrade:
                pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect)
            else:
                pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect, 5)
        else:
            upgrade_point_rect.x -= 60

        text_hp = font.render('HEALTH', True, (200, 200, 200))
        text_hp_highlighted = font.render('HEALTH', True, (100, 200, 200))
        text2_rect = text_hp.get_rect()
        text2_rect.center = draw_screen_rect.center
        text2_rect.x = frame.x + 15

        upgrade_point_rect.centery = text2_rect.centery

        for col in range(1, 4):
            upgrade_point_rect.x += 20
            if col <= self.player.hp_upgrade:
                pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect)
            else:
                pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect, 5)
        else:
            upgrade_point_rect.x -= 60

        text_speed = font.render('SPEED', True, (200, 200, 200))
        text_speed_highlighted = font.render('SPEED', True, (100, 200, 200))
        text3_rect = text_speed.get_rect()
        text3_rect.center = draw_screen_rect.center
        text3_rect.x = frame.x + 15
        text3_rect.y += 1 / 3 * frame.h

        upgrade_point_rect.centery = text3_rect.centery

        for col in range(1, 4):
            upgrade_point_rect.x += 20
            if col <= self.player.speed_upgrade:
                pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect)
            else:
                pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect, 5)

        while True:
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_RETURN:
                #         unpause = True

            mx, my = pygame.mouse.get_pos()

            if text_rect.collidepoint((mx, my)):
                self.draw_screen.blit(text_gunfire_highlighted, text_rect)
                if click:
                    if self.player.gunfire_upgrade < 3:
                        self.player.gunfire_upgrade += 1
                        break
            else:
                self.draw_screen.blit(text_gunfire, text_rect)

            if text2_rect.collidepoint((mx, my)):
                self.draw_screen.blit(text_hp_highlighted, text2_rect)
                if click:
                    if self.player.hp_upgrade < 3:
                        self.player.hp_upgrade += 1
                        break
            else:
                self.draw_screen.blit(text_hp, text2_rect)

            if text3_rect.collidepoint((mx, my)):
                self.draw_screen.blit(text_speed_highlighted, text3_rect)
                if click:
                    if self.player.speed_upgrade < 3:
                        self.player.speed_upgrade += 1
                        break
            else:
                self.draw_screen.blit(text_speed, text3_rect)

            self.refresh_screen()

    def start(self, text):
        self.draw()
        surf = self.font.render(text, False, (255, 255, 255))
        rect = surf.get_rect(center=(int(DRAW_SCREEN_SIZE[0]/2), int(DRAW_SCREEN_SIZE[1]/2)))
        self.draw_screen.blit(surf, rect)
        self.refresh_screen()

        if self.level == 8:
            self.sounds['start_monster'].play()
            timer = 350
        else:
            self.sounds['start'].play()
            timer = START_TIME

        while timer > 0:
            timer -= self.dt
            self.refresh_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()


moving_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    Game()
