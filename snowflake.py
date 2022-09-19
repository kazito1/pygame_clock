
#!/usr/bin/python

import pygame
from pygame.sprite import Sprite

class SnowFlake(Sprite):
    """A class to control a snowflake"""
    def __init__(self, pclock):
        super().__init__()
        self.screen = pclock.screen
        self.settings = pclock.settings
        self.image = pygame.image.load('images/snowflake.png')
        self.rect = self.image.get_rect()

        # Choose the starting position of the cloud
        self.x = 0
        self.rect.x = self.x
        self.y = 0
        self.rect.y = self.y

    def snowflake_finished_falling(self):
        """Returns true if a snowflake has reached the bottom of screen"""
        if (self.rect.y > self.screen.get_rect().height ):
            return True

    def update(self):
        """Move the drop to the bottom of the screen"""
        self.y += self.settings.snowflake_speed
        self.rect.y = self.y