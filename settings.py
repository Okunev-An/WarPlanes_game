class Settings():
    #class for all settings of AlienInvasion Game
    def __init__(self):
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.tries_limit = 3
        self.enemy_hp = 2
        self.max_shots_fired = 5
        self.moving_speed = 9
        self.bg_colour = (255, 255, 255)
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # these settings will change during game session
        self.fleet_direction = 1
        self.moving_speed_y = 1
        self.enemy_points = 40
        self.junkers_speed = 1.5
        self.shot_speed = 2
        self.enemy_shot_speed = 1.2
        self.max_enemy_shots_fired = 3

    def increase_speed(self):
        # increasing game speed and points earning
        self.shot_speed *= self.speedup_scale
        self.enemy_shot_speed *= self.speedup_scale
        self.moving_speed_y *= self.speedup_scale
        self.junkers_speed *= self.speedup_scale
        self.enemy_points = int(self.enemy_points * self.score_scale)
        self.max_enemy_shots_fired += 1
