import sys
import random
from time import sleep

import pygame
from pygame.mixer import Sound

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from asteroid import Asteroid

from button import Button
from scoreboard import Scoreboard
from commands import Commands


class SpaceExplorer:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_hight))
        pygame.display.set_caption("Space Explorere")
        # Load the background image.
        self.background = pygame.image.load('images/stars.bmp').convert()

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create ship, bullets, aliens and asteroids
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.asteroid = Asteroid(self)

        # Create keyboard commands
        self.commands = Commands(self)

        # Create alien fleet and asteroid
        self._create_fleet()
        self._create_asteroid()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Play the sound.
        self.game_sound = Sound('sound/game_sound.wav')
        self.alien_sound = Sound('sound/alien_hit.wav')
        self.asteroid_sound = Sound('sound/asteroid_hit.wav')
        self.ship_sound = Sound('sound/ship_hit.wav')

    def run_game(self):
        """Start the main loop for the game."""
        self.game_sound.play()
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_asteroid()

            self._update_screen()

    def _check_events(self):
       # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.commands.check_keydown_events(event)
            elif event.type == pygame.KEYDOWN:
                self.commands.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.commands.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.blit(self.background, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if self.asteroid:
            self.asteroid.blitme()

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def fire_bullet(self):
        """Create a new bullet and add it to the bullet group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            new_bullet.rect.x = self.ship.rect.right
            new_bullet.rect.y = self.ship.rect.y + self.ship.rect.height / 2
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update(self.ship.rect)

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if (bullet.rect.right > self.screen.get_rect().right):
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        self._check_bullet_asteroid_collisions()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien fleet, with 2 alien ships per row, in 3 rows.
        number_aliens_x = 2
        number_rows = 3

        # Create the fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number+1)

    def _create_alien(self, alien_number, row_number):
        """Create an alien in random position and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = random.randint(
            alien.x + self.screen.get_rect().width / 2, 2*self.screen.get_rect().width - alien.x)
        alien.rect.y = random.randint(
            alien_height, alien_height + self.screen.get_rect().height)
        alien.x = alien.rect.x
        alien.y = alien.rect.y
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update the position of all aliens in the fleet."""
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Get rid of aliens that have disappeared.
        for alien in self.aliens.copy():
            if (alien.rect.left < 0):
                self.aliens.remove(alien)

    def _check_bullet_alien_collisions(self):
        """Check for any bullets that have hit aliens.
        If so, get rid of bullet and alien."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            self.alien_sound.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _check_bullet_asteroid_collisions(self):
        """Check for any bullets that have hit asteroids.
        If so, get rid of  asteroid."""
        if self.asteroid:
            collisions = pygame.sprite.spritecollideany(
                self.asteroid, self.bullets)

            if collisions:
                self.asteroid = None
                self.asteroid_sound.play()
                self.stats.score += self.settings.asteroid_points
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.asteroid:
            # Create new asteroid.
            self._create_asteroid()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien or asteroid."""
        self.ship_sound.play()
        if self.stats.lives_left > 0:
            # Decrement lives_left
            self.stats.lives_left -= 1
            self.sb.prep_lives()

            # Get rid of any remaining aliens, asteroid and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.asteroid = None

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_asteroid(self):
        """Create an asteroid and place it in random position, but within distance from ship larger than asteroid dimensions."""
        asteroid = Asteroid(self)
        asteroid_width, asteroid_height = asteroid.rect.size
        asteroid.x = random.randint(
            -2*asteroid_width, self.screen.get_rect().width + 2*asteroid_width)
        asteroid.y = random.randint(
            -2*asteroid_height, self.screen.get_rect().height - asteroid_height)
        if (abs(self.ship.x - asteroid.x) > asteroid_width and abs(self.ship.y - asteroid.y) > asteroid_height):
            self.asteroid = asteroid

    def _update_asteroid(self):
        """Update the position of asteroid."""
        if self.asteroid:
            self.asteroid.update()

        # Look for asteroid-ship collisions.
        if self.asteroid:
            if self.asteroid.rect.colliderect(self.ship.rect):
                self._ship_hit()

        # Get rid of asteroids that have disappeared.
        if self.asteroid:
            if (self.asteroid.rect.left < 0 or self.asteroid.rect.right > self.screen.get_width() or self.asteroid.rect.top <= 0 or self.asteroid.rect.bottom >= self.screen.get_height()):
                self.asteroid = None

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_lives()

            # Get rid of any remaining aliens, asteroids and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.asteroid = None

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    se = SpaceExplorer()
    se.run_game()
