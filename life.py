import pygame
from pygame.sprite import Sprite


class Life(Sprite):
    """A class to manage the lives left in game."""

    def __init__(self, se_game):
        """Initialize the life."""
        super().__init__()
        self.screen = se_game.screen
        self.settings = se_game.settings
        self.screen_rect = se_game.screen.get_rect()

        # Load the life image and get its rect.
        self.image = pygame.image.load('images/fire.bmp')
        self.image = pygame.transform.scale(self.image, (21, 32))
        self.rect = self.image.get_rect()
