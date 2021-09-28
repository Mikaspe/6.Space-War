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


def close():
    pygame.quit()
    sys.exit(0)


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.set_num_channels(50)

        self.textures = {}  # Textures(png) from img directory
        self.load_textures()

        self.sounds = {}  # Sounds(wav) from sounds directory
        self.load_sounds()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # Screen for display => surface
        pygame.display.set_caption('Space-War')
        # draw_screen is a surface which'll be scaled and drawn on display screen
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.draw_screen_rect = self.draw_screen.get_rect()

        self.clock = pygame.time.Clock()  # Helps track time
        self.dt = 1  # delta time

        self.player = Player('player1')
        self.enemies = []
        self.projectiles = []
        self.animations = pygame.sprite.Group()

        self.ENEMYMOVE = pygame.USEREVENT  # User event for moving enemy
        pygame.time.set_timer(self.ENEMYMOVE, ENEMY_MOVE_RATIO)
        self.PROJECTILEMOVE = pygame.USEREVENT  # User event for moving projectiles
        pygame.time.set_timer(self.PROJECTILEMOVE, PROJECTILE_MOVE_RATIO)

        self.start_end_title_font = pygame.font.Font('OpenSans-Bold.ttf', 100)

        self.timer = 0  # Used for player shooting ratio
        self.timer2 = 0  # Used for heart beating when hp is low
        
        self.border = 70  # Border of moving enemies

        self.level = 1
        self.max_level = 8
        self.go_to_main_menu = False

        self.level_switch()

    def load_textures(self):
        for img in os.listdir('img'):
            if img.endswith('.png'):
                self.textures[img.replace('.png', '')] = pygame.image.load(f'img/{img}')  # => surface

        for img in os.listdir('img/background'):
            self.textures[img.replace('.png', '')] = pygame.image.load(f'img/background/{img}')  # => surface

    def load_sounds(self):
        for sound in os.listdir('sounds'):
            self.sounds[sound.replace('.wav', '')] = pygame.mixer.Sound(f'sounds/{sound}')  # => sound

    def level_switch(self):
        """Main loop"""
        while True:
            self.go_to_main_menu = False
            self.main_menu()
            self.level = 1
            self.player.reset()
            while True:
                self.player.hp_update()
                self.player.speed_update()
                self.player.gunfire_update()
                self.start(f'Level {self.level}')  # Draw start title
                self.game()
                self.enemies.clear()
                self.projectiles.clear()
                self.animations.empty()
                if self.go_to_main_menu:
                    break

    def game(self):
        """Generation of levels and game processing"""
        # Generating enemies spaceships
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
                for x in range(1, 5):
                    enemy = Enemy(x*100 + self.border, y*75, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 6:
            enemy_style = 3
            for y in range(4):
                if y >= 2:
                    enemy_style = 2
                for x in range(6):
                    enemy = Enemy(x*100 + self.border, y*75 + 40, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 7:
            for y in range(4):
                for x in range(8):
                    if y <= 2:
                        enemy_style = 3
                    elif y > 2 and x in range(3, 5):
                        enemy_style = 3
                    else:
                        enemy_style = 2
                    enemy = Enemy(x*100 + self.border, y*75 + 40, enemy_style)
                    self.enemies.append(enemy)
        elif self.level == 8:
            enemy_style = 4
            self.border = 10
            enemy = Enemy(DRAW_SCREEN_SIZE[0]/2, 170, enemy_style)
            enemy.shoot_ratio = 50
            self.enemies.append(enemy)

        start_seq = False  # Boss fight(lvl 8) berserker sequence
        timer = 0  # Used in boss berserker sequence
        timer2 = 0  # Used for shot ratio in boss berserker sequence
        played_berserker_sound = False
        played_bosslowhp_sound = False

        while True:
            self.check_keys()
            self.check_events()

            # Changing enemies move direction when farthest reach self.border
            self.enemies.sort(key=operator.attrgetter('rect.x'))  # Sorting enemies by x position
            if self.enemies[0].rect.x < self.border:  # Left border
                for enemy in self.enemies:
                    enemy.direction = 'right'
            elif self.enemies[-1].rect.x > DRAW_SCREEN_SIZE[0] - self.border - self.enemies[-1].rect.w:  # Right border
                for enemy in self.enemies:
                    enemy.direction = 'left'

            # Generating enemies projectiles
            for enemy in self.enemies:
                if enemy.style == 1:
                    if random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser-enemy'].play()
                        projectile = Projectile(enemy.rect.centerx, enemy.rect.centery, 'enemy1')
                        self.projectiles.append(projectile)
                elif enemy.style == 2:
                    if random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser-enemy'].play()
                        projectile = Projectile(enemy.rect.centerx, enemy.rect.centery, 'enemy2')
                        self.projectiles.append(projectile)
                elif enemy.style == 3:
                    if random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser-enemy'].play()
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
                        self.sounds['laser-enemy'].play()
                        projectile = Projectile(enemy.rect.centerx - 155, enemy.rect.centery, 'enemy-smallball')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx + 155, enemy.rect.centery, 'enemy-smallball')
                        self.projectiles.append(projectile)
                    elif random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser-enemy'].play()
                        projectile = Projectile(enemy.rect.centerx - 115, enemy.rect.centery + 145, 'enemy4')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx + 115, enemy.rect.centery + 145, 'enemy4')
                        self.projectiles.append(projectile)
                    elif random.randint(1, enemy.shoot_ratio) == 1:
                        self.sounds['laser-enemy'].play()
                        projectile = Projectile(enemy.rect.centerx - 120, enemy.rect.centery - 105, 'enemy4')
                        self.projectiles.append(projectile)
                        projectile = Projectile(enemy.rect.centerx + 120, enemy.rect.centery - 105, 'enemy4')
                        self.projectiles.append(projectile)

                    if start_seq:  # Boss sequence in berserker mode
                        if not played_berserker_sound:
                            self.sounds['enemy-berserker'].play()
                            self.sounds['enemy-berserker2'].play()
                            played_berserker_sound = True

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
                                self.sounds['laser-enemy'].play()
                                projectile = Projectile(enemy.rect.centerx - 155, enemy.rect.centery, 'enemy-smallball')
                                self.projectiles.append(projectile)
                                projectile = Projectile(enemy.rect.centerx + 155, enemy.rect.centery, 'enemy-smallball')
                                self.projectiles.append(projectile)
                        elif 1600 < timer < 3000:
                            if timer2 < 100:
                                self.sounds['laser-enemy'].play()
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
                                self.explosion = Explosion(*enemy.rect.center)
                                self.explosion.animate()
                                self.animations.add(self.explosion)
                                self.enemies.remove(enemy)
                                for enemy in self.enemies:  # Speed of enemies increase when number of them decrease
                                    enemy.speed += 0.2
                            break

            if self.player.hp == 1 and not played_bosslowhp_sound:
                self.sounds['low-hp'].play()
                played_bosslowhp_sound = True
            elif self.player.hp <= 0:
                self.sounds['game-over'].play()
                self.end('TRY AGAIN')
                break
            elif self.level == 8 and not self.enemies:
                self.sounds['killed-monster'].play()
                self.end('YOU WIN')
                self.go_to_main_menu = True
                break
            elif not self.enemies:
                self.sounds['win'].play()
                self.end('LEVEL COMPLETED')
                self.upgrade_menu()
                self.level += 1
                break

            self.draw_game()
            self.refresh_screen()
            if self.go_to_main_menu:
                break

    def check_keys(self):
        """Check keyboard keys"""
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
                self.sounds['laser-player'].play()
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
        """Built-in and user events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies:
                    enemy.move()
            if event.type == self.PROJECTILEMOVE:
                for projectile in self.projectiles:
                    projectile.move()

    def draw_game(self):
        """Drawing game images"""
        self.draw_screen.blit(self.textures[f'background{self.level}'], (0, 0))
        self.draw_screen.blit(self.player.get_image(), self.player.rect)

        # Explosion animation
        for sprite in self.animations:
            sprite.update(1.6)
        self.animations.draw(self.draw_screen)

        for enemy in self.enemies:
            self.draw_screen.blit(enemy.image, enemy)
            if self.level == 8:
                frame_rect = pygame.Rect((0, 10), (enemy.hp, 3))
                frame_rect.centerx = self.draw_screen_rect.centerx
                pygame.draw.rect(self.draw_screen, (200, 0, 0), frame_rect, 2)

        for projectile in self.projectiles:
            self.draw_screen.blit(projectile.image, projectile)
        for heart in range(self.player.hp):
            self.draw_screen.blit(self.textures['heart'], (heart*12-4, 5))

        if self.player.hp == 1:
            self.timer2 += self.dt
            if self.timer2 < 20:
                self.draw_screen.blit(self.textures['heart-black'], (-4, 5))
            else:
                self.draw_screen.blit(self.textures['heart'], (-4, 5))
                if self.timer2 > 40:
                    self.timer2 = 0

        self.draw_current_level()  # Draw current level in top-right corner

    def refresh_screen(self):
        """Scale resolution, update display and delta time"""
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)  # Resize to new resolution
        self.screen.blit(scaled, (0, 0))  # Draw onto display screen
        pygame.display.update()  # Update portions of the screen for software displays
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

    def end(self, text):
        """Draw end title"""
        self.draw_game()

        text_surf = self.start_end_title_font.render(text, False, (255, 255, 255))
        text_rect = text_surf.get_rect()
        text_rect.center = (DRAW_SCREEN_SIZE[0]/2, DRAW_SCREEN_SIZE[1]/2)
        self.draw_screen.blit(text_surf, text_rect)

        if self.level == 8:
            timer = 200
        else:
            timer = END_TIME

        while timer > 0:
            self.refresh_screen()
            timer -= self.dt

    def main_menu(self):
        # Frame
        frame_rect = pygame.Rect((0, 0), (150*1.61, 150))
        frame_rect.center = self.draw_screen_rect.center

        # Text Start
        font = pygame.font.Font('freesansbold.ttf', 40)
        text_start = font.render('Start', True, (200, 200, 200))
        text_start_highlighted = font.render('Start', True, (100, 200, 200))
        text_start_rect = text_start.get_rect(center=self.draw_screen_rect.center)
        text_start_rect.y -= 1/3 * frame_rect.h

        # Text Spaceship
        text_spaceship = font.render('Spaceship', True, (200, 200, 200))
        text_spaceship_highlighted = font.render('Spaceship', True, (100, 200, 200))
        text_spaceship_rect = text_spaceship.get_rect(center=self.draw_screen_rect.center)

        # Text Exit
        text_exit = font.render('Exit', True, (200, 200, 200))
        text_exit_highligted = font.render('Exit', True, (100, 200, 200))
        text_exit_rect = text_exit.get_rect(center=self.draw_screen_rect.center)
        text_exit_rect.y += 1/3 * frame_rect.h

        # Main menu navigation(keyboard and mouse)
        menu_pos = 1
        m1 = m2 = m3 = True
        while True:
            self.draw_screen.blit(self.textures['background1'], (0, 0))
            pygame.draw.rect(self.draw_screen, (200, 200, 200), frame_rect, 5)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close()
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
            if text_start_rect.collidepoint((mx, my)) and m1:
                menu_pos = 1
                m1 = False
                m2 = True
                m3 = True
            elif text_spaceship_rect.collidepoint((mx, my)) and m2:
                menu_pos = 2
                m1 = True
                m2 = False
                m3 = True
            elif text_exit_rect.collidepoint((mx, my)) and m3:
                menu_pos = 3
                m1 = True
                m2 = True
                m3 = False

            if menu_pos == 1:
                self.draw_screen.blit(text_start_highlighted, text_start_rect)
                if click:
                    break  # Leave main menu, start the game
            else:
                self.draw_screen.blit(text_start, text_start_rect)

            if menu_pos == 2:
                self.draw_screen.blit(text_spaceship_highlighted, text_spaceship_rect)
                if click:
                    self.spaceship_choose()  # Choose spaceship model
            else:
                self.draw_screen.blit(text_spaceship, text_spaceship_rect)

            if menu_pos == 3:
                self.draw_screen.blit(text_exit_highligted, text_exit_rect)
                if click:
                    close()  # Close window
            else:
                self.draw_screen.blit(text_exit, text_exit_rect)

            self.refresh_screen()

    def pause_menu(self):
        # Frame
        frame_rect = pygame.Rect((0, 0), (150 * 1.61, 150))
        frame_rect.center = self.draw_screen_rect.center

        # Text continue
        font = pygame.font.Font('freesansbold.ttf', 40)
        text_continue = font.render('Continue', True, (200, 200, 200))
        text_continue_highlighted = font.render('Continue', True, (100, 200, 200))
        text_continue_rect = text_continue.get_rect(center=self.draw_screen_rect.center)
        text_continue_rect.y -= 1/3 * frame_rect.h

        # Text Main menu
        text_main_menu = font.render('Main menu', True, (200, 200, 200))
        text_main_menu_highlighted = font.render('Main menu', True, (100, 200, 200))
        text_main_menu_rect = text_main_menu.get_rect(center=self.draw_screen_rect.center)

        # Text exit
        text_exit = font.render('Exit', True, (200, 200, 200))
        text_exit_highlighted = font.render('Exit', True, (100, 200, 200))
        text_exit_rect = text_exit.get_rect(center=self.draw_screen_rect.center)
        text_exit_rect.y += 1/3 * frame_rect.h

        # Pause menu navigation(keyboard and mouse)
        menu_pos = 1
        m1 = m2 = m3 = True
        while True:
            self.draw_game()
            pygame.draw.rect(self.draw_screen, (200, 200, 200), frame_rect, 5)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
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
            if text_continue_rect.collidepoint((mx, my)) and m1:
                menu_pos = 1
                m1 = False
                m2 = True
                m3 = True
            elif text_main_menu_rect.collidepoint((mx, my)) and m2:
                menu_pos = 2
                m1 = True
                m2 = False
                m3 = True
            elif text_exit_rect.collidepoint((mx, my)) and m3:
                menu_pos = 3
                m1 = True
                m2 = True
                m3 = False

            if menu_pos == 1:
                self.draw_screen.blit(text_continue_highlighted, text_continue_rect)
                if click:
                    break  # Continue game
            else:
                self.draw_screen.blit(text_continue, text_continue_rect)

            if menu_pos == 2:
                self.draw_screen.blit(text_main_menu_highlighted, text_main_menu_rect)
                if click:
                    self.go_to_main_menu = True
                    break
            else:
                self.draw_screen.blit(text_main_menu, text_main_menu_rect)

            if menu_pos == 3:
                self.draw_screen.blit(text_exit_highlighted, text_exit_rect)
                if click:
                    close()
            else:
                self.draw_screen.blit(text_exit, text_exit_rect)

            self.refresh_screen()

    def spaceship_choose(self):
        """Player can choose spaceship model"""
        # Title
        font = pygame.font.Font('freesansbold.ttf', 40)
        text_spaceship = font.render('Choose spaceship:', True, (200, 200, 200))
        text_rect = text_spaceship.get_rect()
        text_rect.center = DRAW_SCREEN_SIZE[0]/2, DRAW_SCREEN_SIZE[1]/2 - 60

        # Spaceships
        spacehip1_rect = self.player.textures['player1-choosen'].get_rect()
        spacehip1_rect.x = DRAW_SCREEN_SIZE[0]/2 - 50
        spacehip1_rect.y = DRAW_SCREEN_SIZE[1]/2

        spacehip2_rect = self.player.textures['player2-choosen'].get_rect()
        spacehip2_rect.x = DRAW_SCREEN_SIZE[0]/2 - 200
        spacehip2_rect.y = DRAW_SCREEN_SIZE[1]/2

        spacehip3_rect = self.player.textures['player3-choosen'].get_rect()
        spacehip3_rect.x = DRAW_SCREEN_SIZE[0]/2 + 100
        spacehip3_rect.y = DRAW_SCREEN_SIZE[1]/2

        # Spaceship choose navigation(keyboard and mouse)
        menu_pos = 1
        m1 = m2 = m3 = True
        while True:
            self.draw_screen.blit(self.textures['background1'], (0, 0))
            self.draw_screen.blit(text_spaceship, text_rect)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close()
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
            elif spacehip2_rect.collidepoint((mx, my)) and m2:
                menu_pos = 2
                m1 = True
                m2 = False
                m3 = True
            elif spacehip3_rect.collidepoint((mx, my)) and m3:
                menu_pos = 3
                m1 = True
                m2 = True
                m3 = False

            if menu_pos == 1:
                self.draw_screen.blit(self.player.textures['player1-choosen'], (spacehip1_rect.x, spacehip1_rect.y))
                if click:
                    self.player.change_spaceship('player1')
                    break  # Go back to main menu
            else:
                self.draw_screen.blit(self.player.textures['player1-stop'], (spacehip1_rect.x, spacehip1_rect.y))

            if menu_pos == 2:
                self.draw_screen.blit(self.player.textures['player2-choosen'], (spacehip2_rect.x, spacehip2_rect.y))
                if click:
                    self.player.change_spaceship('player2')
                    break  # Go back to main menu
            else:
                self.draw_screen.blit(self.player.textures['player2-stop'], (spacehip2_rect.x, spacehip2_rect.y))

            if menu_pos == 3:
                self.draw_screen.blit(self.player.textures['player3-choosen'], (spacehip3_rect.x, spacehip3_rect.y))
                if click:
                    self.player.change_spaceship('player3')
                    break  # Go back to main menu
            else:
                self.draw_screen.blit(self.player.textures['player3-stop'], (spacehip3_rect.x, spacehip3_rect.y))

            self.refresh_screen()

    def upgrade_menu(self):
        """Upgrade menu is displayed after finishing each level.
        Player can upgrade one of the abilities"""
        self.draw_screen.blit(self.textures['background1'], (0, 0))
        self.draw_current_level()  # Draw current level in top-right corner
        # Frame of upgrade menu
        frame_rect = pygame.Rect((0, 0), (290, 160))
        frame_rect.center = self.draw_screen_rect.center
        pygame.draw.rect(self.draw_screen, (200, 200, 200), frame_rect, 5)

        # Gunfire text
        font = pygame.font.SysFont('swiss721', 38)
        text_gunfire = font.render('GUNFIRE', True, (200, 200, 200))
        text_gunfire_highlighted = font.render('GUNFIRE', True, (100, 200, 200))
        left_pos_of_text = frame_rect.left + 15
        text_gunfire_rect = text_gunfire.get_rect(left=left_pos_of_text, centery=frame_rect.centery - 45)

        # Health text
        text_hp = font.render('HEALTH', True, (200, 200, 200))
        text_hp_highlighted = font.render('HEALTH', True, (100, 200, 200))
        text_hp_rect = text_hp.get_rect(left=left_pos_of_text, centery=frame_rect.centery)

        # Speed text
        text_speed = font.render('SPEED', True, (200, 200, 200))
        text_speed_highlighted = font.render('SPEED', True, (100, 200, 200))
        text_speed_rect = text_speed.get_rect(left=left_pos_of_text, centery=frame_rect.centery + 45)

        # Drawing points of upgrades
        upgrade_point_rect = pygame.Rect((0, 0), (15, 15*1.61))
        upgrade_point_rect.center = (frame_rect.centerx + 50, text_gunfire_rect.centery)
        space_beetwen_points = 20
        for upgrade in (self.player.gunfire_upgrade, self.player.hp_upgrade, self.player.speed_upgrade):
            for col in range(1, 4):
                upgrade_point_rect.x += space_beetwen_points
                if col <= upgrade:
                    pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect)
                else:
                    pygame.draw.rect(self.draw_screen, (200, 200, 200), upgrade_point_rect, 5)
            else:
                upgrade_point_rect.x -= space_beetwen_points * 3
            upgrade_point_rect.y += 45

        # Menu navigation(keyboard and mouse)
        menu_pos = 1
        m1 = m2 = m3 = True
        while True:

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.go_to_main_menu = True
                        break
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
            if text_gunfire_rect.collidepoint((mx, my)) and m1:
                menu_pos = 1
                m1 = False
                m2 = True
                m3 = True
            elif text_hp_rect.collidepoint((mx, my)) and m2:
                menu_pos = 2
                m1 = True
                m2 = False
                m3 = True
            elif text_speed_rect.collidepoint((mx, my)) and m3:
                menu_pos = 3
                m1 = True
                m2 = True
                m3 = False

            if menu_pos == 1:
                self.draw_screen.blit(text_gunfire_highlighted, text_gunfire_rect)
                if click:
                    if self.player.gunfire_upgrade < 3:
                        self.player.gunfire_upgrade += 1
                        break
            else:
                self.draw_screen.blit(text_gunfire, text_gunfire_rect)

            if menu_pos == 2:
                self.draw_screen.blit(text_hp_highlighted, text_hp_rect)
                if click:
                    if self.player.hp_upgrade < 3:
                        self.player.hp_upgrade += 1
                        break
            else:
                self.draw_screen.blit(text_hp, text_hp_rect)

            if menu_pos == 3:
                self.draw_screen.blit(text_speed_highlighted, text_speed_rect)
                if click:
                    if self.player.speed_upgrade < 3:
                        self.player.speed_upgrade += 1
                        break
            else:
                self.draw_screen.blit(text_speed, text_speed_rect)

            self.refresh_screen()

    def start(self, title):
        """Draw level number and play sound at the beginning of level"""
        self.draw_game()
        text_title = self.start_end_title_font.render(title, False, (255, 255, 255))
        text_title_rect = text_title.get_rect(center=self.draw_screen_rect.center)
        self.draw_screen.blit(text_title, text_title_rect)
        self.refresh_screen()

        if self.level == 8:
            self.sounds['start_monster'].play()
            timer = 350
        else:
            self.sounds['start'].play()
            timer = START_TIME

        break_loop = False
        while timer > 0 and not break_loop:
            timer -= self.dt
            self.refresh_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        break_loop = True
                        break

    def draw_current_level(self):
        """Draw current level in top-right corner"""
        font = pygame.font.SysFont('swiss721', 17)
        text_level = font.render(f'{self.level}/{self.max_level}', True, (200, 200, 200))
        text_level_rect = text_level.get_rect()
        text_level_rect.center = (DRAW_SCREEN_SIZE[0] - 20, 15)
        self.draw_screen.blit(text_level, text_level_rect)


if __name__ == '__main__':
    Game()
