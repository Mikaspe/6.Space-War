import operator

import pygame

from state import State
from game_objects.player import Player
from game_objects.enemy import Enemy
from game_objects.explosion import Explosion


class Game(State):
    def __init__(self, data):
        self.data = data
        State.__init__(self)
        self.next = 'end'

        self.player = Player(self.data, 'player1')
        self.enemies = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.animations = pygame.sprite.Group()

    def cleanup(self):  # Wywołane raz przed przejsciem do next stanu
        pass  # Tutaj nie dalem czyszczenia bo po przejsciu w pause czyscilo

    def startup(self):  # Wywołane raz na początku tego stanu
        if self.previous != 'pause':
            self.enemies.empty()
            self.enemy_projectiles.empty()
            self.player.projectiles.empty()
            self.animations.empty()
            self.player.hp_update()
            self.player.speed_update()
            self.player.gunfire_update()
            self.player.gunfire_update()
            self.player.style = self.data.player_spaceship_style
            self.enemies.add(*[Enemy(self.data, *enemy_arg) for enemy_arg in
                               self.data.enemies_args[self.data.level]])  # Można uprościć aby było bardziej czytelne
            self.timer_heart_beating = 0
            self.played_lowhp_sound = False

    def get_event(self, event):  # Zbiera eventy z control i reaguje na nie w swoj sposob
        self.player.get_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next = 'pause'
                self.done = True

        # if event.type == MOVE:  # UWAGA, tutaj jest opcja przesłania evantu do każdego obiektu enemy i tam wykonanie move
        #     self.enemies.update()

    def update(self, keys, dt):  # Updatuje to co sie dzieje w tym stanie

        if self.data.hp > 0 and self.enemies:
            self.player.update(keys, dt)
            self.enemies.update(dt)
            self.__keep_enemies_in_window()
            self.__enemy_projectiles_gen(dt)
            self.__enemy_projectiles_remove()
            self.__player_projectiles_remove()
        else:
            self.next = 'end'
            self.done = True

        if keys[pygame.K_n]:
            self.next = 'end'
            self.done = True

        self.draw(dt)  # Rysuje

    def draw(self, dt):  # Rysowanie
        self.data.SCREEN.blit(self.data.GFX[f'background{self.data.level}'], (0, 0))
        self.player.draw()
        # Explosion animation
        for animation in self.animations:
            animation.update(1.6)
        self.animations.draw(self.data.SCREEN)  # Draw all explosion animations

        self.enemies.draw(self.data.SCREEN)
        self.enemy_projectiles.draw(self.data.SCREEN)
        self.__draw_current_level()
        self.__draw_player_hearts(dt)

    def __draw_current_level(self) -> None:
        """Draws current level in top-right corner"""
        font = pygame.font.SysFont('swiss721', 17)
        text_level = font.render(f'{self.data.level}/{self.data.max_level}', True, (200, 200, 200))
        text_level_rect = text_level.get_rect()
        text_level_rect.center = (self.data.WIN_SIZE[0] - 20, 15)
        self.data.SCREEN.blit(text_level, text_level_rect)

    def __draw_player_hearts(self, dt):

        if self.data.hp > 1:
            for heart in range(self.data.hp):
                self.data.SCREEN.blit(self.data.GFX['heart'], (heart * 12 - 4, 5))
        elif self.data.hp == 1:
            self.timer_heart_beating += dt
            if self.timer_heart_beating < 200:
                self.data.SCREEN.blit(self.data.GFX['heart'], (-4, 5))
            elif self.timer_heart_beating > 400:
                self.timer_heart_beating = 0

            if not self.played_lowhp_sound:
                self.data.SFX['low-hp'].play()
                self.played_lowhp_sound = True

    def __keep_enemies_in_window(self):
        # Changing enemies move direction when farthest reaches self.border
        enemies_lst = self.enemies.sprites()
        enemies_lst.sort(key=operator.attrgetter('rect.x'))
        if enemies_lst[0].rect.left < 0:
            for enemy in self.enemies:
                enemy.direction = 'right'
        elif enemies_lst[-1].rect.right > self.data.WIN_SIZE[0]:
            for enemy in self.enemies:
                enemy.direction = 'left'

    def __enemy_projectiles_gen(self, dt):
        for enemy in self.enemies:
            self.enemy_projectiles.add(enemy.projectile_generation(dt))

        self.enemy_projectiles.update(dt)

    def __enemy_projectiles_remove(self):
        for projectile in self.enemy_projectiles:
            if projectile.rect.top > self.data.WIN_SIZE[1]:
                self.enemy_projectiles.remove(projectile)
            if pygame.sprite.collide_mask(self.player, projectile):
                if projectile.style == 'enemy-ball':
                    self.data.SFX['ball-hit'].play()
                    self.enemy_projectiles.remove(projectile)
                    self.data.hp -= 1
                elif projectile.style == 'enemy-smallbal':
                    self.data.SFX['ball-hit'].play()
                    self.enemy_projectiles.remove(projectile)
                    self.data.hp -= 1
                elif projectile.style.startswith('enemy'):
                    self.data.SFX['hit'].play()
                    self.enemy_projectiles.remove(projectile)
                    self.data.hp -= 1

    def __player_projectiles_remove(self):
        for projectile in self.player.projectiles:
            for enemy in self.enemies:
                if pygame.sprite.collide_mask(enemy, projectile):
                    self.player.projectiles.remove(projectile)
                    enemy.hp -= 1
                    if enemy.hp > 0:
                        self.data.SFX['hit'].play()
                    elif enemy.hp == 0:
                        self.data.SFX['destroyed'].play()
                        self.explosion = Explosion(*enemy.rect.center)
                        self.explosion.animate()
                        self.animations.add(self.explosion)
                        self.enemies.remove(enemy)
                        for enemy in self.enemies:  # Speed of enemies increase when number of them decrease
                            enemy.speed += 0.01
                    break


