#!/usr/bin/python

import pygame

class Sun:
    """A class to represent the sun on screen"""

    def __init__(self, pclock):
        self.pclock = pclock
        self.screen = pclock.screen

        # Load the sun image
        self.image = pygame.image.load('images/sun.png')
        self.rect = self.image.get_rect()

        # Start the sun outside the screen but centered
        self.rect.x = (self.screen.get_rect().width - self.rect.width)/2
        self.rect.y = self.screen.get_rect().height + 1

        # The initial sunset, initial sunrise and  initial noon
        self.sunrise_time = self.pclock.sunrise_time
        self.sunset_time = self.pclock.sunset_time
        self.halfday_time = int( self.sunrise_time
            + ( self.sunset_time - self.sunrise_time )/2 )


        # The sky should have day colors when the sun reaches this
        # position
        self.complete_sunrise_pos = (self.screen.get_rect().height 
            - self.rect.height)

        # The maximum height that the sun should reach on screen (noon)
        self.zenith = 20


    def get_sun_position(self,current_time):
        """Calculates the position of the sun based on time"""
        # We use the line equation: y = mt + b

        # Calculate the slope first
        # m = (y2 - y1)/(t2 - t1)
        if (current_time < self.halfday_time):
            slope_m = (( self.zenith - self.screen.get_rect().height + 1 ) 
                / (self.halfday_time - self.sunrise_time ))
        else:
            slope_m = (( self.screen.get_rect().height + 1 - self.zenith )
                / (self.sunset_time - self.halfday_time ))

        # Calculate the value of b
        # b = y - mx
        b = self.zenith - slope_m * self.halfday_time

        # Calculate the position based on current_time
        y = slope_m * current_time + b
        return y

    def update(self):
        """
        Move the sun to a new position and gets latets sunrise
        and sunset
        """
        # Update the sunset, sunrise and noon
        self.sunrise_time = self.pclock.sunrise_time
        self.sunset_time = self.pclock.sunset_time
        self.halfday_time = int( self.sunrise_time
            + ( self.sunset_time - self.sunrise_time )/2 )
        self.rect.y = self.get_sun_position(self.pclock.current_time)

    def blitme(self):
        """Draw the sun in the current location"""
        self.screen.blit(self.image, self.rect)