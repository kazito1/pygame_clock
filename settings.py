#!/usr/bin/python
import json

class Settings:
    """A class to store all settings for PyGameClock"""

    def __init__(self):
        """Initialize the clock settings"""
        try:
            with open("config/pygame_clock.json") as f:
                self.set_settings_from_config_file(json.load(f))
        except:
            self.set_defaults()

    def set_settings_from_config_file(self, all_settings):
        """Sets the settings from config file"""
        self.set_defaults()
        if('fullscreen' in all_settings):
            self.fullscreen = int(all_settings["fullscreen"])
        if('use_photos' in all_settings):
            self.show_photos = int(all_settings["use_photos"])
        if('screen_width' in all_settings):
            self.screen_width = int(all_settings["screen_width"])
        if('screen_height' in all_settings):
            self.screen_height = int(all_settings["screen_height"])
        if('bg_color' in all_settings):
            self.bg_color = all_settings["bg_color"]
        if('clock_font' in all_settings):
            self.clock_font = all_settings["clock_font"]
        if('time_face_percent' in all_settings):
            self.time_face_percent = int(abs(all_settings["time_face_percent"]))
        if('date_face_percent' in all_settings):
            self.date_face_percent = int(abs(all_settings["date_face_percent"]))
        if('weather_face_percent' in all_settings):
            self.weather_face_percent = int(abs(
                    all_settings["weather_face_percent"]))
        if('day_text_color' in all_settings):
            self.day_text_color = all_settings["day_text_color"]
        if('night_text_color' in all_settings):
            self.night_text_color = all_settings["night_text_color"]
        if('time_format' in all_settings):
            self.time_format = all_settings["time_format"]
        if('date_format' in all_settings):
            self.date_format = all_settings["date_format"]
        if('temperature_units' in all_settings):
            self.temperature_units = all_settings["temperature_units"]
        if('api_key' in all_settings):
            self.api_key = all_settings["api_key"]
        if('queries_per_minute' in all_settings):
            self.queries_per_minute = int(all_settings["queries_per_minute"])
        if('day_color' in all_settings):
            self.day_color = all_settings["day_color"]
        if('night_color' in all_settings):
            self.night_color = all_settings["night_color"]
        if('cloud_speed' in all_settings):
            self.cloud_speed = all_settings["cloud_speed"]
        if('minimum_percent_of_last_cloud' in all_settings):
            self.minimum_percent_of_last_cloud = (
                all_settings["minimum_percent_of_last_cloud"])
        if('raindrop_speed' in all_settings):
            self.raindrop_speed = all_settings["raindrop_speed"]
        if('snowflake_speed' in all_settings):
            self.snowflake_speed = all_settings["snowflake_speed"]
        if('latitude' in all_settings):
            self.latitude = all_settings["latitude"]
        if('longitude' in all_settings):
            self.longitude = all_settings["longitude"]

        # Make sure we are not exceeding 100 percent of screen with the
        # size of the data shown on screen and if so, 
        # substract the extra so we are 100 percent at maximum
        if(self.time_face_percent + self.date_face_percent 
                + self.weather_face_percent > 100):
            to_remove = int((100 - (self.time_face_percent
                + self.date_face_percent 
                + self.weather_face_percent))/3)+1
            self.time_face_percent = self.time_face_percent - to_remove
            self.date_face_percent = self.date_face_percent - to_remove
            self.weather_face_percent = self.weather_face_percent - to_remove
        
    def set_defaults(self):
        """Sets the defaults for all settings"""
        # Sky colors
        self.day_color = (135,206,235)
        self.night_color = (12,20,69)

        # Cloud settings
        self.cloud_speed = 0.1
        self.minimum_percent_of_last_cloud = 10

        # Rain settings
        self.raindrop_speed = 15

        # Snowflake settings
        self.snowflake_speed = 3

        # Screen settings
        self.fullscreen = 1
        self.show_photos = 1
        self.screen_width = 800
        self.screen_height = 480
        self.bg_color = (0,0,0)

        # ClockFace Settings
        self.clock_font = "quicksand"
        self.time_face_percent = 30
        self.date_face_percent = 10
        self.weather_face_percent = 10
        self.night_text_color = (255,255,255)
        self.day_text_color = (0,0,0)
        self.time_format = "%H:%M:%S"
        self.date_format = "%A, %B %d"

        # Weather Settings
        # Api key for OWM
        self.temperature_units = "celsius"
        self.api_key = "xxxxxxxxxxxxxxxxxxxxxxxx"
        self.queries_per_minute = 2