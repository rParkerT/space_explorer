import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, se_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = se_game.screen
        self.settings = se_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (52, 29))
        self.rect = self.image.get_rect()

        # Start each new alien near the top right of the screen.
        self.rect.x = self.screen.get_rect().right
        self.rect.y = self.screen.get_rect().top

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the alien to the left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
