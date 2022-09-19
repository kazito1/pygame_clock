#!/usr/bin/python
class Sky:
    """A class to manage the sky color"""
    def __init__(self, pclock):

        self.pclock = pclock
        self.sun = pclock.sun
        self.settings = pclock.settings
        self.screen = pclock.screen
        
        self.day_color=self.settings.day_color
        self.night_color=self.settings.night_color

        self.complete_sunrise_pos = self.sun.complete_sunrise_pos
        self.sun_hidden_pos = self.screen.get_rect().height + 1

    def get_current_color(self):
        """Calculates the color of the sky based on the sun position"""

        self.max_red, self.max_green, self.max_blue = self.day_color
        self.min_red, self.min_green, self.min_blue = self.night_color

        # Obtain y = mx + b for the three colors

        # Slopes:
        slope_red = (self.min_red - self.max_red) / (self.sun_hidden_pos 
            - self.complete_sunrise_pos)
        slope_green = (self.min_green - self.max_green) / (self.sun_hidden_pos 
            - self.complete_sunrise_pos)
        slope_blue = (self.min_blue - self.max_blue) / (self.sun_hidden_pos 
            - self.complete_sunrise_pos)

        # b value b = y - mx
        b_red = self.min_red - slope_red * self.sun_hidden_pos
        b_green = self.min_green - slope_green * self.sun_hidden_pos
        b_blue = self.min_blue - slope_blue * self.sun_hidden_pos

        y_red = int( slope_red * self.sun.get_sun_position(
            self.pclock.current_time) + b_red )
        y_green = int( slope_green * self.sun.get_sun_position(
            self.pclock.current_time) + b_green )
        y_blue = int( slope_blue * self.sun.get_sun_position(
            self.pclock.current_time) + b_blue )

        return (y_red, y_green, y_blue)

    def paint_sky(self):
        """Paints the sky"""
        if (self.sun.get_sun_position(self.pclock.current_time) >= 
                self.screen.get_rect().height):
            # Night
            self.current_color = self.night_color
        elif (self.sun.get_sun_position(self.pclock.current_time) 
                >= self.complete_sunrise_pos
                and  self.sun.get_sun_position(self.pclock.current_time)
                <= self.screen.get_rect().height):
            # going to sunrise or sunset
            self.current_color = self.get_current_color()
        else:
            # day
            self.current_color = self.day_color
        self.screen.fill(self.current_color)
