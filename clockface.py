#!/usr/bin/python
import pygame.font
import time

class ClockFace:
    """A class to draw the clock face"""

    def __init__(self, pclock):
        """Initialize face attributes"""
        self.pclock = pclock
        self.screen = pclock.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pclock.settings

        # Font settings
        self.day_text_color = pclock.settings.day_text_color
        self.night_text_color = pclock.settings.night_text_color
        self.time_font_size = int(self.screen.get_rect().height
                * self.settings.time_face_percent/100)
        self.date_font_size = int(self.screen.get_rect().height
                * self.settings.date_face_percent/100)
        self.weather_font_size = int(self.screen.get_rect().height
                * self.settings.weather_face_percent/100)
        
        # First Time for current_time
        self.current_time = 0
        self.sunrise_time = 20000
        self.sunset_time = 60000

        self.prep_face()

    def get_text_color(self):
        """Returns the text color to use depending of day or night"""
        if (self.current_time > self.sunrise_time
                and self.current_time <= self.sunset_time):
            return self.day_text_color
        else:
            return self.night_text_color


    def prep_time(self):
        """Prepares the time part of the face"""
        text_color = self.get_text_color()
        self.font = pygame.font.SysFont(self.settings.clock_font,
                self.time_font_size)
        time_str = time.strftime(self.settings.time_format,self.local_time)
        self.time_image = self.font.render(time_str, True, text_color)
        self.time_rect = self.time_image.get_rect()
        self.time_rect.left = ( self.screen.get_rect().width 
            - self.time_image.get_rect().width ) / 2
        self.time_rect.top = ( self.screen.get_rect().height 
            - self.time_image.get_rect().height ) / 2

    def prep_date(self):
        """Prepares the date part of the face at top of the screen"""
        text_color = self.get_text_color()
        self.font = pygame.font.SysFont(self.settings.clock_font,
                self.date_font_size)
        date_str = time.strftime(self.settings.date_format,self.local_time)
        self.date_image = self.font.render(date_str, True, text_color)
        self.date_rect = self.date_image.get_rect()
        self.date_rect.left = ( self.screen.get_rect().width 
            - self.date_image.get_rect().width ) / 2
        # We want the date centered above the time string
        self.date_rect.top = ( self.time_rect.top 
            - self.date_image.get_rect().height ) / 2
        

    def prep_weather(self):
        """Prepares the weather part of the face at the bottom of """
        """the screen"""
        text_color = self.get_text_color()
        self.font = pygame.font.SysFont(self.settings.clock_font,
                self.weather_font_size)
        temperature = int(self.pclock.weather.weather.temperature(
                self.pclock.settings.temperature_units)['temp'])
        location = f"{self.pclock.location.city}, {self.pclock.location.region}"
        weather_status = f"{self.pclock.weather.weather.detailed_status}"
        if (self.pclock.settings.temperature_units == 'celsius'):
            symbol_str = '°C'
        elif (self.pclock.settings.temperature_units == 'fahrenheit'):
            symbol_str = '°F'
        else:
            symbol_str = 'K'
        weather_str = f"{temperature}{symbol_str} at {location}. {weather_status.capitalize()}"
        self.weather_image = self.font.render(weather_str, True, 
            text_color)
        self.weather_rect = self.weather_image.get_rect()
        self.weather_rect.left = ( self.screen.get_rect().width 
            - self.weather_image.get_rect().width ) / 2
        # We want the weather centered below the time string
        pixels_to_add = (self.screen.get_rect().height 
                        - self.time_rect.bottom
                        ) / 2
        self.weather_rect.top = self.time_rect.bottom + pixels_to_add

    def prep_face(self):
        """Turn all the things in face into a rendered image"""
        # self.current_time and self.local_time can be checked from outside
        # the class
        self.current_time = time.time()
        self.local_time = time.localtime(self.current_time)
        if (hasattr(self.pclock,'sunrise_time')):
            self.sunrise_time = self.pclock.sunrise_time
        if (hasattr(self.pclock,'sunset_time')):
            self.sunset_time = self.pclock.sunset_time
        self.prep_time()
        self.prep_date()
        self.prep_weather()

    def show_face(self):
        """Draw face of the clock"""
        self.screen.blit(self.time_image, self.time_rect)
        self.screen.blit(self.date_image, self.date_rect)
        self.screen.blit(self.weather_image, self.weather_rect)
