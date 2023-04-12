import pygame.event
import sys

from button import Button


class Commands:
    """A class for handling keyboard events."""

    def __init__(self, se_game):
        """Initialize keyboard events handling."""
        self.se_game = se_game
        self.settings = se_game.settings
        self.stats = se_game.stats
        self.ship = se_game.ship

    def check_keydown_events(self, event):
        """ Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left.
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            # Move the ship up.
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # Move the ship down.
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            # Fire bullet.
            self.se_game.fire_bullet()
        elif event.key == pygame.K_q:
            # Exit the game.
            if self.stats.high_score > self.settings.ultimate_high:
                self._update_ultimate_high_score()
            sys.exit()

    def check_keyup_events(self, event):
        """ Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left.
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            # Move the ship up.
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            # Move the ship down.
            self.ship.moving_down = False

    def _update_ultimate_high_score(self):
        """Update the ultimate high score in settings of the game."""
        with open('settings.py', 'r') as file:
            # read a list of lines
            lines = file.readlines()
        file.close()

        outputfile = open('settings.py', 'w')

        new_value = "        self.ultimate_high = {}\n".format(
            self.stats.high_score)

        # replace ultimate high for new value and write everything back
        for line in lines:
            if "self.ultimate_high = " in line:
                outputfile.write(line.replace(str(line), new_value))
            else:
                outputfile.write(line)

        outputfile.close()
