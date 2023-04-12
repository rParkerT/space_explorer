class Settings:
    """A class to store all settings for Space Explorer."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_hight = 600
        self.bg_color = (0, 0, 130)

        # Lives settings
        self.lives_limit = 5

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 6
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point value increases
        self.score_scale = 1.5

        # The ultimate high result
        self.ultimate_high = 32015

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 3.0
        self.bullet_speed = 3.5
        self.alien_speed = 1.5
        self.asteroid_speed = 0.2

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = -1

        # Scoring
        self.alien_points = 10
        self.asteroid_points = 50

    def increase_speed(self):
        """Increase speed settings, asteroid and alien point values."""
        if self.alien_speed < 5.0:
            self.ship_speed *= self.speedup_scale
            self.bullet_speed *= self.speedup_scale
            self.alien_speed *= self.speedup_scale
            self.asteroid_speed *= self.speedup_scale
            self.alien_points = int(self.alien_points*self.score_scale)
            self.asteroid_points = int(self.asteroid_points*self.score_scale)
