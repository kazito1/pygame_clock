#!/usr/bin/python

# ToDo, make difference between day normal clouds, day rain/snow clouds, 
# night normal clouds and night rain/snow clouds

from random import seed
from random import randrange

import pygame
from pygame.sprite import Sprite

class Cloud(Sprite):
    """A class to represent a single cloud in all the sky"""

    def __init__(self, pclock):
        super().__init__()
        self.screen = pclock.screen
        self.settings = pclock.settings
        self.pclock = pclock
        seed()

        # ToDo: Perhaps for next version
        #
        # Ability to choose different types of clouds depending
        # on conditions, e.g. cloud_day_rain, cloud_day_clear, etc
        #
        # Something like:
        # if (self.pclock.weather.rain):
        #   if (self.pclock.current_time > self.pclock.sunrise_time
        #       and self.pclock.current_time < self.pclock.sunset_time)
        #   image_name = 'cloud_day_rain.png'
        #  etc...

        # Load the cloud image and set its rect attribute.
        if (self.pclock.current_time >= self.pclock.sunrise_time
                and self.pclock.current_time < self.pclock.sunset_time):
            self.image = pygame.image.load('images/cloud_day.png')
        else:
            self.image = pygame.image.load('images/cloud_night.png')

        self.rect = self.image.get_rect()

        # Choose the starting position of the cloud
        self.rect.x = - self.rect.width
        self.x = self.rect.x
        self.rect.y = randrange(0,self.screen.get_rect().height)

    def cloud_finished_travel(self):
        """Checks if a cloud has disappeared from screen"""
        if (self.rect.x > self.screen.get_rect().width ):
            return True

    def cloud_size(self):
        return self.rect.width * self.rect.height

    def update(self):
        """Move the cloud to the right"""
        self.x += self.settings.cloud_speed
        self.rect.x = self.x
