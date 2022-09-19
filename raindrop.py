
#!/usr/bin/python
# Slight rain: Less than 0.5 mm per hour. Moderate rain: Greater than 
# 0.5 mm per hour, but less than 4.0 mm per hour. Heavy rain: Greater 
# than 4 mm per hour, but less than 8 mm per hour. Very heavy rain: 
# Greater than 8 mm per hour.

# Get current rain amount on a location
# Also rain amount is a dict, with keys: 1h an 3h, containing the mms of
# rain fallen in the last 1 and 3 hours

# from pyowm.owm import OWM
# owm = OWM('your-api-key')
# mgr = owm.weather_manager()
# rain_dict = mgr.weather_at_place('Berlin,DE').weather.rain
# rain_dict['1h']
# rain_dict['3h']

import pygame
from pygame.sprite import Sprite

class RainDrop(Sprite):
    """A class to control a raindrop"""
    def __init__(self, pclock):
        super().__init__()
        self.screen = pclock.screen
        self.settings = pclock.settings
        self.image = pygame.image.load('images/raindrop.png')
        self.rect = self.image.get_rect()

        # Choose the starting position of the cloud
        self.x = 0
        self.rect.x = self.x
        self.y = 0
        self.rect.y = self.y

    def drop_finished_falling(self):
        """Returns true if a drop has reached the bottom of screen"""
        if (self.rect.y > self.screen.get_rect().height ):
            return True

    def update(self):
        """Move the drop to the bottom of the screen"""
        self.y += self.settings.raindrop_speed
        self.rect.y = self.y