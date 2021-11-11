import operator

import pygame

from state import State
from game_objects.player import Player
from game_objects.enemy import Enemy
from game_objects.explosion import Explosion


class Game(State):
    """Actual game state. Called in 'Control' object in the control module."""
    def __init__(self, data) -> None:
        State.__init__(self)
        self.data = data
        self.next = 'end'

        self.player = Player(self.data, 'player1')  # Player spaceship object
        self.enemies = pygame.sprite.Group()  # Group of all enemie spaceships
        self.enemy_projectiles = pygame.sprite.Group()  # Group of all enemie projectiles
        self.animations = pygame.sprite.Group()  # Group of all current animations

    def cleanup(self) -> None:
        """State cleanup. Called once when current state flips to the next one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        pass

    def startup(self) -> None:
        """State objects preparing. Called once when current state flips to the this one.
        Called in the '__flip_state' method in 'Control' object('control' module).
        """
        if self.previous != 'pause':
            self.enemies.empty()  # Removing all enemies
            self.enemy_projectiles.empty()  # Removing all enemy projectiles
            self.player.projectiles.empty()  # Removing all player projectiles
            self.animations.empty()  # Removing all animations
            self.player.hp_update()
            self.player.speed_update()
            self.player.gunfire_update()
            self.player.style = self.data.player_spaceship_style  # Player spaceship model

            # Generating enemy spaceship from data
            for enemy_arg in self.data.enemies_args[self.data.level]:
                self.enemies.add(Enemy(self.data, *enemy_arg))  # enemy_arg is a tuple(x_pos, y_pos, style)

            self.timer_heart_beating = 0  # Timer for heart 'beating' when player hp is low
            self.played_lowhp_sound = False

    def get_event(self, event: pygame.event) -> None:
        """Events handling passed as argument by 'Control' object.
        Called in the '__event_loop' method in 'Control' object('control' module).

        Parameters:
            event: PyGame events
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Pause game
                self.next = 'pause'
                self.done = True
        self.player.get_event(event)

    def update(self, keys: pygame.key, dt: int) -> None:
        """Main processing of the state.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            keys: state of all keyboard buttons
            dt: delta time in ms
        """
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

        if keys[pygame.K_n]:  # For tests only                                                                    !!!!!!!!
            self.next = 'end'
            self.done = True

    def draw(self, dt: int) -> None:
        """Draws game objects on the screen.
        Called in the '__update' method in 'Control' object('control' module).

        Parameters:
            dt: delta time in ms
        """
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

        if self.data.level == 8 and self.enemies.has():
            self.__draw_boss_healthbar()

    def __draw_current_level(self) -> None:
        """Draws current level('level/max_level') in the top-right corner.
        Called in the '__draw' method.
        """
        font = pygame.font.SysFont('swiss721', 17)
        text_level = font.render(f'{self.data.level}/{self.data.max_level}', True, (200, 200, 200))
        text_level_rect = text_level.get_rect()
        text_level_rect.center = (self.data.WIN_SIZE[0] - 20, 15)
        self.data.SCREEN.blit(text_level, text_level_rect)

    def __draw_player_hearts(self, dt: int) -> None:
        """Draws player health points as hearts in the top-left corner.
        Called in the '__draw' method.

        Parameters:
            dt: delta time in ms
        """
        if self.data.hp > 1:
            for heart in range(self.data.hp):
                self.data.SCREEN.blit(self.data.GFX['heart'], (heart * 12 - 4, 5))
        elif self.data.hp == 1:
            if not self.played_lowhp_sound:
                self.data.SFX['low-hp'].play()
                self.played_lowhp_sound = True

            self.timer_heart_beating += dt
            if self.timer_heart_beating < 200:  # Heart image recurrently appears and disapears
                self.data.SCREEN.blit(self.data.GFX['heart'], (-4, 5))
            elif self.timer_heart_beating > 400:
                self.timer_heart_beating = 0

    def __draw_boss_healthbar(self) -> None:
        """Draws boss healthbar in the top of the screen.
        Called in the '__draw' method.
        """
        frame_rect = pygame.Rect((0, 10), (self.enemies.sprites()[0].hp, 3))
        frame_rect.centerx = self.data.SCREEN_RECT.centerx
        pygame.draw.rect(self.data.SCREEN, (200, 0, 0), frame_rect, 2)

    def __keep_enemies_in_window(self) -> None:
        """Changing enemies move direction when farthest reaches definied border.
        Called in  the 'update' method.
        """
        enemies_lst = self.enemies.sprites()
        enemies_lst.sort(key=operator.attrgetter('rect.x'))
        if enemies_lst[0].rect.left < 0:  # Enemie reaches left border
            for enemy in self.enemies:
                enemy.direction = 'right'
        elif enemies_lst[-1].rect.right > self.data.WIN_SIZE[0]:  # Enemie reaches right border
            for enemy in self.enemies:
                enemy.direction = 'left'

    def __enemy_projectiles_gen(self, dt: int) -> None:
        """Generation of projectiles shot by enemies.
        Called in the 'update' method.

        Parameters:
            dt: delta time in ms
        """
        for enemy in self.enemies:
            self.enemy_projectiles.add(enemy.projectile_generation(dt))
        self.enemy_projectiles.update(dt)

    def __enemy_projectiles_remove(self) -> None:
        """Removing enemy projectiles when out of the screen or strike player spaceship.
        Called in the 'update' method.
        """
        for projectile in self.enemy_projectiles:
            if projectile.rect.top > self.data.WIN_SIZE[1]:  # Projectile out of the screen
                self.enemy_projectiles.remove(projectile)
            if pygame.sprite.collide_mask(self.player, projectile):  # Projectile strike a player spaceship
                if projectile.style == 'enemy-ball':
                    self.data.SFX['ball-hit'].play()
                    self.enemy_projectiles.remove(projectile)
                    self.data.hp -= 2
                elif projectile.style == 'enemy-smallbal':
                    self.data.SFX['ball-hit'].play()
                    self.enemy_projectiles.remove(projectile)
                    self.data.hp -= 1
                elif projectile.style.startswith('enemy'):
                    self.data.SFX['hit'].play()
                    self.enemy_projectiles.remove(projectile)
                    self.data.hp -= 1

    def __player_projectiles_remove(self) -> None:
        """Removing player projectiles when strike enemy spaceship.
        Called in the 'update' method.
        """
        for projectile in self.player.projectiles:
            for enemy in self.enemies:
                if pygame.sprite.collide_mask(enemy, projectile):
                    self.player.projectiles.remove(projectile)
                    enemy.hp -= 1
                    if enemy.hp > 0:
                        self.data.SFX['hit'].play()
                    elif enemy.hp == 0:
                        self.data.SFX['destroyed'].play()
                        self.explosion = Explosion(self.data, *enemy.rect.center)
                        self.explosion.animate()
                        self.animations.add(self.explosion)
                        self.enemies.remove(enemy)
                        for enemy in self.enemies:  # Speed of enemies increase when number of them decrease
                            enemy.speed += 0.01
                    break


