class GameStats:
    """Track statistics for Alien invasion."""

    def __init__(self, se_game):
        """Initialize statistics."""
        self.settings = se_game.settings
        self.reset_stats()
        # Start Alien Invasion in an active state.
        self.game_active = False
        # High score should never be reset.
        self.high_score = self.settings.ultimate_high

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.lives_limit
        self.score = 0
        self.level = 1
