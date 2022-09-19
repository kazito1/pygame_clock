#import pyowm
import sys
from pyowm import OWM, commons

class WeatherAtLocation:
    """A simple class to get the weather at a location"""

    def __init__(self,pclock):
        """Initializes values"""
        self.api_key = pclock.settings.api_key
        self.owm = OWM(self.api_key)
        self.mgr = self.owm.weather_manager()
        self.latitude = pclock.latitude
        self.longitude = pclock.longitude

    def get_current_weather(self):
        """Gets the current weather"""
        try:
            self.observation =  self.mgr.weather_at_coords(self.latitude, 
            self.longitude)
            self.weather = self.observation.weather
        except (commons.exceptions.UnauthorizedError) as error:
            print(error)
            sys.exit(1)
