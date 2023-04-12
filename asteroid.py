import pygame
import random


class Asteroid():
    """A class to represent a asteroid."""

    def __init__(self, se_game):
        """Initialize the asteroid and set its starting position."""
        super().__init__()
        self.screen = se_game.screen
        self.settings = se_game.settings

        # Load the asteroid image and set its rect attribute.
        self.image = pygame.image.load('images/asteroid.bmp')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

        # Start each new asteroid near the top right of the screen.
        self.rect.x = self.screen.get_rect().right
        self.rect.y = self.screen.get_rect().top

        # Store the asteroid's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the asteroid at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the asteroid."""
        self.x += ((self.x - self.screen.get_rect().centerx) *
                   self.settings.asteroid_speed) / 100.
        self.y -= ((self.y-self.screen.get_rect().centery) *
                   self.settings.asteroid_speed) / 100.
        self.rect.x = self.x
        self.rect.y = self.y
