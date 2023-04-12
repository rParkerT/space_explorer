import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, se_game):
        """Initialize the ship and sets its starting position."""
        super().__init__()
        self.screen = se_game.screen
        self.settings = se_game.settings
        self.screen_rect = se_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()

        # Start each new ship at the center of the screen.
        self.rect.center = self.screen_rect.center

        # Store a decimal value for the ship's horizontal and vertical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update ship's position based on the movement flag."""
        # Update the ship's x and y value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += (self.settings.ship_speed*0.1) + \
                self.settings.ship_speed
        if self.moving_left and self.rect.left > 20:
            self.x -= (self.settings.ship_speed*0.1) + self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += (self.settings.ship_speed*0.1) + self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= (self.settings.ship_speed*0.1) + self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.center = self.screen_rect.center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
