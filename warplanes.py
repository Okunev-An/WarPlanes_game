import sys
import pygame
from junkers import Junkers
from shot import Shot
from enemy import Enemy
from settings import Settings
from stats import Stats
from button import Button
from time import sleep
from scoreboard import Scoreboard
from info import Info

class WarPlanes:
    # a class for resourses and game management
    def __init__(self):
        # initializes game session and builds game resourses
        pygame.init()
        self.settings = Settings()
        # storing game statistics
        self.stats = Stats(self)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Warplanes")
        self.bg_color = self.settings.bg_colour
        self.hp = self.settings.enemy_hp
        self.junkers = Junkers(self)
        self.shots = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # game scoreboard
        self.sb = Scoreboard(self)
        self.play_button = Button(self, "START", (0, -100))
        self.info_button = Button(self, "INFO", (0, 100))
        self.pause_button = Button(self, "Continue")
        self._create_sky()
        self.info = Info(self)
        pygame.mixer.music.load('music.wav')
        self.shot_sound = pygame.mixer.Sound('shot.ogg')
        self.explosion_sound = pygame.mixer.Sound('explosion.ogg')
    def _create_sky(self):
        # creating enemy fleet
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        avail_space_y = self.settings.screen_height
        # calculating fleet size
        number_enemies_y = avail_space_y // (2*enemy_height)
        number_cols = 5
        for col_number in range(number_cols):
            for enemy_number in range(number_enemies_y):
                self._create_enemy(enemy_number, col_number)

    def _create_enemy(self, enemy_number, col_number):
        # creating enemy and adding to enemy fleet
        enemy = Enemy(self)
        enemy.hp = self.hp
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = 3*enemy_width + (2 * enemy_width * col_number)
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.rect.height + (2*enemy_number*enemy.rect.height)
        self.enemies.add(enemy)

    def run_game(self):
        # main game session
        while True:
            self._check_events()
            if self.stats.game_active and not self.stats.game_paused:
                self.junkers.update()
                self._update_shots()
                self._enemy_fire()
                self._update_enemies()
            self._update_screen()

    def _check_play_button(self, mouse_pos):
        # launching new game while pressing play button
        if self.play_button.rect.collidepoint(mouse_pos)\
                and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            pygame.mixer.music.play(-1)
            self.enemies.empty()
            self.shots.empty()
            self.enemy_shots.empty()
            self._create_sky()
            self.junkers.center_plane()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_high_score()
            self.sb.prep_ships()

    def _check_info_button(self, mouse_pos):
        # open information menu
        if self.info_button.rect.collidepoint(mouse_pos) \
                and not self.stats.game_active:
            self.stats.info_open = True


    def _check_pause_button(self, mouse_pos):
        # resuming a paused game session
        if self.pause_button.rect.collidepoint(mouse_pos)\
                                and self.stats.game_paused:
            self.stats.game_paused = False
            pygame.mixer.music.unpause()

    def junkers_hit(self):
        # working with junkers-enemy collisions
        if self.stats.lives_left > 0:
            self.stats.lives_left -= 1
            self.enemies.empty()
            self.shots.empty()
            self._create_sky()
            self.junkers.center_plane()
            self.sb.prep_ships()
            sleep(1.5)
        else:
            # ending game session
            self.junkers.center_plane()
            pygame.mixer.music.pause()
            self.stats.game_active = False

    def _check_events(self):
        # Tracking events from keyboard and mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_pause_button(mouse_pos)
                self._check_info_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.junkers.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.junkers.moving_left = True
        elif event.key == pygame.K_UP:
            self.junkers.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.junkers.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._open_fire()
        elif event.key == pygame.K_RETURN:
            self.stats.info_open = False
        elif event.key == pygame.K_p:
            if self.stats.game_active:
                pygame.mixer.music.pause()
                self.stats.game_paused = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.junkers.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.junkers.moving_left = False
        elif event.key == pygame.K_UP:
            self.junkers.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.junkers.moving_down = False

    def _update_shots(self):
        # working with shots: if shot hits target or
        # the edge of the screen, it will be deleted
        self.shots.update()
        for shot in self.shots.copy():
            if shot.rect.right <= 0:
                self.shots.remove(shot)
        self._check_shot_enemy_collisions()
        self.enemy_shots.update()
        for shot in self.enemy_shots.copy():
            if shot.rect.left >= self.screen_rect.right:
                self.enemy_shots.remove(shot)
        self._check_junkers_shots_collisions()

    def _check_junkers_shots_collisions(self):
        # working with collisions between enemies' shots and junkers
        collisions = pygame.sprite.spritecollide(self.junkers, self.enemy_shots, True)
        if collisions:
            self.junkers_hit()

    def _check_shot_enemy_collisions(self):
        # working with collisions between shots and enemies
        # if enemy is hit, remove the bullet
        collisions = pygame.sprite.groupcollide(self.shots, self.enemies, True, False)
        if collisions:
            for enemies in collisions.values(): #values
                for enemy in enemies:
                    if enemy.hp <= 1:
                        # remove the enemy, play sound
                        self.explosion_sound.play()
                        self.enemies.remove(enemy)
                        self.stats.score += self.settings.enemy_points  # * len(enemies)
                else:
                    # reduce enemy's hp by 1
                    enemy.get_damage()
                    enemy.hp -= 1

            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_high_score()
        if not self.enemies:
            # remove fired bullets, leveling up
            self.shots.empty()
            self.stats.level += 1
            self.settings.increase_speed()
            self.sb.prep_level()
            self._create_sky()

    def _update_enemies(self):
        self._check_fleet_edges()
        for enemy in self.enemies.copy():
        # if enemy reaches base, you are lost
            if enemy.rect.right > self.screen_rect.right:
                self.junkers_hit()
        # player must not collide with enemies
        if pygame.sprite.spritecollideany(self.junkers, self.enemies):
            self.junkers_hit()
        self.enemies.update()

    def _check_fleet_edges(self):
        # reacts on reaching an edge by the alien
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # moving fleet right and change its direction
        for enemy in self.enemies.sprites():
            enemy.rect.x += self.settings.moving_speed
        self.settings.fleet_direction *= -1

    def _open_fire(self):
        if len(self.shots) < self.settings.max_shots_fired:
            self.shot_sound.play()
            new_shot = Shot(self)
            self.shots.add(new_shot)

    def _enemy_fire(self):
        if len(self.enemy_shots) < self.settings.max_enemy_shots_fired:
            shot = Shot(self, direction=-1, shooter='enemy')
            self.enemy_shots.add(shot)


    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.junkers.blitme()
        for shot in self.shots.sprites():
            shot.draw_shot()
        for shot in self.enemy_shots.sprites():
            shot.draw_shot()
        self.enemies.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.info_button.draw_button()
        if self.stats.game_paused:
            self.pause_button.draw_button()
        if self.stats.info_open:
            self.info._prep_txt()
        pygame.display.flip()


if __name__ == '__main__':
    fd = WarPlanes()
    fd.run_game()
