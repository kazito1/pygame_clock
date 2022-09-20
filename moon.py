#!/usr/bin/python

import pygame

class Moon:
    """A class to represent the sun on screen"""

    def __init__(self, pclock):
        self.pclock = pclock
        self.screen = pclock.screen

        # Load the sun image
        self.image = pygame.image.load('images/moon.png')
        self.rect = self.image.get_rect()

        # Start the moon outside the screen but centered
        self.rect.x = (self.screen.get_rect().width - self.rect.width)/2
        self.rect.y = self.screen.get_rect().height + 1

        # These initial values get fixed by the update method

        # The sunset, sunrise and middle of the night
        self.sunset_time = self.pclock.sunset_time
        # Since we don't know the exact sunrise time for next day at the
        # beginning of the night, we are going to approximate it based
        # in the previous day
        self.sunrise_time = self.pclock.sunrise_time + 86400 
        self.halfnight_time = int( self.sunset_time
            + ( self.sunrise_time - self.sunset_time )/2 )

        # The maximum height that the moon should reach on screen
        self.zenith = 20


    def get_moon_position(self,current_time):
        """Calculates the position of the moon based on time"""
        # We use the line equation: y = mt + b

        # Calculate the slope first
        # m = (y2 - y1)/(t2 - t1)
        if (current_time < self.halfnight_time):
            slope_m = (( self.zenith - self.screen.get_rect().height + 1 ) 
                / (self.halfnight_time - self.sunset_time ))
        else:
            slope_m = (( self.screen.get_rect().height + 1 - self.zenith )
                / (self.sunrise_time - self.halfnight_time ))

        # Calculate the value of b
        # b = y - mx
        b = self.zenith - slope_m * self.halfnight_time

        # Calculate the position based on current_time
        y = slope_m * current_time + b
        return y

    def update(self):
        """Move the moon to a new position"""
        if (self.pclock.current_time > self.pclock.sunset_time
                and self.pclock.sunset_time > self.pclock.sunrise_time):
            # The sunrise time has not been updated yet
            # Since we don't know the exact sunrise time until it gets updated
            # we are going to approximate it based in the previous day
            self.sunset_time = self.pclock.sunset_time
            self.sunrise_time = self.pclock.sunrise_time + 86400
            self.halfnight_time = int( self.sunset_time
                + ( self.sunrise_time - self.sunset_time )/2 )
        elif (self.pclock.current_time < self.pclock.sunrise_time
                and self.pclock.current_time < self.pclock.sunset_time):
            # Both sunset and sunrise have been updated, 
            # but we are still on night
            self.sunset_time = self.pclock.sunset_time - 86400
            self.sunrise_time = self.pclock.sunrise_time
            self.halfnight_time = int( self.sunset_time
                + ( self.sunrise_time - self.sunset_time )/2 )
        else:
            # Moon is no longer on screen
            # We can safely update both values and guess the next
            # halfnight time
            self.sunrise_time = self.pclock.sunrise_time
            self.sunset_time = self.pclock.sunset_time
            self.halfnight_time = int( self.sunset_time
                + ( self.sunrise_time + 86400 - self.sunset_time )/2 )
        new_moon_position = self.get_moon_position(self.pclock.current_time)
        self.rect.y = new_moon_position

    def blitme(self):
        """Draw the moon in the current location"""
        self.screen.blit(self.image, self.rect)
