#!/usr/bin/python
import sys

import pygame

from settings import Settings
from sun import Sun
from moon import Moon
from sky import Sky
from cloud import Cloud
from raindrop import RainDrop
from snowflake import SnowFlake
from clockface import ClockFace
from mylocation import MyLocation
from weatheratlocation import WeatherAtLocation

class PyGameClock:
    """Overall class to create the clock"""

    def __init__(self):
        """Initialize the clock and create resources"""
        pygame.init()

        self.settings = Settings()
        self.location = MyLocation(self)
        self.latitude = self.location.lat
        self.longitude = self.location.long
        self.weather = WeatherAtLocation(self)

        # WINDOW MODE
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))

        pygame.display.set_caption("PyGame Clock")

        # Get weather for the first time
        self.weather.get_current_weather()

        # Create an instance of the clock face
        self.clock_face = ClockFace(self)

        # Set background color
        self.bg_color = self.settings.bg_color

        # Initialize animated background objects
        self._initialize_raindrop_snowflake_width()
        self.current_time = self.clock_face.current_time
        self.sunrise_time = self.weather.weather.sunrise_time()
        self.sunset_time = self.weather.weather.sunset_time()
        self.cloud_percent = self.weather.weather.clouds
        self.sun = Sun(self)
        self.moon = Moon(self)
        self.sky = Sky(self)
        self.clouds = pygame.sprite.Group()
        self.raindrop_snow_odd_even = 0
        self.rainy_weather = pygame.sprite.Group()
        self.snowy_weather = pygame.sprite.Group()
        self.last_time_cloud_created = 0

        # Reset the queries dictionary
        self.weather_queries = {}
        self._reset_queries_dictionary()
        if (self.settings.show_photos):
            self._choose_background()
            self.last_background_image = ""
            self._load_background()


    def run_clock(self):
        """Start the main loop of the clock"""
        self.last_minute=0
        while True:
            self._check_events()
            self.clock_face.prep_face()
            self._query_weather()
            self.current_time = self.clock_face.current_time
            self.sunrise_time = self.weather.weather.sunrise_time()
            self.sunset_time = self.weather.weather.sunset_time()
            self.cloud_percent = self.weather.weather.clouds
            self.rain = self.weather.weather.rain
            self.snow = self.weather.weather.snow
            if(self.settings.show_photos):
                self._load_background()
            else:
                self.sun.update()
                self.moon.update()
                self._update_clouds()
                self._update_rainy_weather()
                self._update_snowy_weather()
            self._update_screen()
            self._verify_queries_dictionary()

    def _check_events(self):
        """Respond to keypresses"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        if ( event.key == pygame.K_q or event.key == pygame.K_ESCAPE ):
            sys.exit()

    def _update_screen(self):
        """Updates what we see of the clock in screen"""
        if (self.settings.show_photos):
            if (self.background_image=="image_not_found"):
                self.screen.fill(self.settings.bg_color)
            else:
                self.screen.blit(self.background, (0, 0))
        else:
            self.sky.paint_sky()
            self.sun.blitme()
            self.moon.blitme()
            self.clouds.draw(self.screen)
            self.rainy_weather.draw(self.screen)
            self.snowy_weather.draw(self.screen)
        self.clock_face.show_face()
        pygame.display.flip()

    def _reset_queries_dictionary(self):
        """
        Resets the flags for the seconds where the query against weather
        OWM api has been done
        """
        self.period = int(60/self.settings.queries_per_minute)
        for i in range(0,59,self.period):
            self.weather_queries[i] = 0

    def _verify_queries_dictionary(self):
        """Verifies if a reset to the queries dictionary is required"""
        current_minute=self.clock_face.local_time.tm_min
        if (self.clock_face.local_time.tm_sec == 0 and 
                current_minute != self.last_minute):
            self._reset_queries_dictionary()
            self.last_minute=self.clock_face.local_time.tm_min

    def _choose_background(self):
        """Chooses the appropriate bg image depending on the weather"""
        if ((self.weather.weather.weather_code >= 500 and
                self.weather.weather.weather_code <= 531) or
                (self.weather.weather.weather_code >= 300 and
                self.weather.weather.weather_code <= 321 )
                ):
            self.background_image="rain"
        elif (self.weather.weather.weather_code == 800):
            self.background_image="clear"
        elif (self.weather.weather.weather_code >= 801 and
                self.weather.weather.weather_code <= 804 ):
            self.background_image="clouds"
        elif (self.weather.weather.weather_code == 741):
            self.background_image="fog"
        elif (self.weather.weather.weather_code == 721):
            self.background_image="haze"
        elif (self.weather.weather.weather_code == 701):
            self.background_image="mist"
        elif (self.weather.weather.weather_code >= 600 and
                self.weather.weather.weather_code <= 622 ):
            self.background_image="snow"
        elif (self.weather.weather.weather_code == 781 or
                self.weather.weather.weather_code == 900):
            self.background_image="tornado"
        elif (self.weather.weather.weather_code == 901 or 
                (self.weather.weather.weather_code >= 960 and
                self.weather.weather.weather_code <= 961 )):
            self.background_image="storm"
        elif (self.weather.weather.weather_code == 902 or
                self.weather.weather.weather_code <= 962 ):
            self.background_image="hurricane"

        if (self.clock_face.current_time >= self.sunrise_time and
                self.clock_face.current_time < self.sunset_time):
            self.background_image = self.background_image + "_day"
        else:
            self.background_image = self.background_image + "_night"

    def _query_weather(self):
        """Checks if we need to query about the weather"""
        if (self.clock_face.local_time.tm_sec in self.weather_queries):
            if (self.weather_queries[self.clock_face.local_time.tm_sec] == 0 and 
                    self.clock_face.local_time.tm_sec % self.period == 0):
                self.weather_queries[self.clock_face.local_time.tm_sec] = 1
                try:
                    self.weather.get_current_weather()
                except:
                    pass
                self._choose_background()
        
    def _load_background(self):
        """Loads the requested image"""
        if (self.background_image != self.last_background_image):
            try:
                self.background = pygame.image.load("images/"+self.background_image+".png")
            except:
                self.background_image = "image_not_found"
            self.last_background_image = self.background_image

    def _update_clouds(self):
        """
            Creates a cloud if required and allowed and runs the
            update function for cloud sprites
        """
        distance_to_next_cloud = self._distance_for_next_cloud()
        if (self.cloud_percent):
            if (self.clouds):
                leftmost_cloud = self._get_leftmost_cloud()
                if (self._get_percent_visible_of_cloud(leftmost_cloud) 
                        > self.settings.minimum_percent_of_last_cloud
                        and leftmost_cloud.rect.right >= 
                        self._distance_for_next_cloud()
                        ):
                    self._create_cloud()
            else:
                self._create_cloud()
        aux_clouds = self.clouds.copy()
        for cloud in aux_clouds:
            if (cloud.cloud_finished_travel()):
                cloud.kill()
        self.clouds.update()

    def _get_percent_visible_of_cloud(self,cloud):
        """Gets the visible percent of a cloud"""
        if (cloud.rect.right > 0):
            if (cloud.rect.right > cloud.rect.width):
                visible_width = cloud.rect.width
            else:
                visible_width = cloud.rect.right
            percent_visible  = visible_width*100/cloud.rect.width
        else:
            percent_visible = 0
        return percent_visible

    def _get_leftmost_cloud(self):
        """Gets the letftmost cloud"""
        leftmost_x = self.settings.screen_width
        for cloud in self.clouds:
            if (cloud.x < leftmost_x):
                leftmost_x = cloud.x
                leftmost_cloud = cloud
        return leftmost_cloud

    def _distance_for_next_cloud(self):
        """Calculates the number of pixels required for next cloud"""
        pass
        foo = self.cloud_percent
        # Maximum distance between clouds is 20% of screen
        maximum_distance = 0.20*self.settings.screen_width
        # Let's do a line y = mx + b:
        #  distance_between_clouds = (-maximum_distance/100)*percent
        #       + maximum_distance
        distance_between_clouds = (-1*maximum_distance/100*self.cloud_percent
            + maximum_distance)
        return distance_between_clouds
        
    def _create_cloud(self):
        """Adds a new cloud"""
        cloud = Cloud(self)
        self.clouds.add(cloud)

    def _initialize_raindrop_snowflake_width(self):
        """Initializes the width of a raindrop and a snowflake"""
        raindrop = RainDrop(self)
        self.raindrop_width = raindrop.rect.width
        raindrop.kill()
        snowflake = SnowFlake(self)
        self.snowflake_width = snowflake.rect.width
        snowflake.kill()

    def _raindrop_spacing(self):
        """
        Calculates the space between each one of the drops based on the
        mm of water
        """
        # Slight rain: Less than 0.5 mm per hour. Moderate rain: Greater than 
        # 0.5 mm per hour, but less than 4.0 mm per hour. Heavy rain: Greater 
        # than 4 mm per hour, but less than 8 mm per hour. Very heavy rain: 
        # Greater than 8 mm per hour.
        spacing = 0
        if (self.rain):
            if (float(self.rain['1h']) < 0.5):
                # slight rain
                spacing = 2
                pass
            elif (float(self.rain['1h']) >= 0.5 and float(self.rain['1h']) < 4):
                # moderate rain
                spacing = 1.5
                pass
            elif (float(self.rain['1h']) >= 4 and float(self.rain['1h']) < 8):
                # heavy rain
                spacing = 1
                pass
            elif (float(self.rain['1h']) >= 8):
                # very heavy rain
                spacing = 0.5
                pass
        return spacing

    def _create_raindrop_row(self):
        """Creates a row of rain drops"""
        if (self.rain and self._last_raindrop_row_is_on_screen()):
            number_raindrops_x = (self.settings.screen_width 
                // ( ( self._raindrop_spacing() * self.raindrop_width ) 
                + self.raindrop_width ) )
            # Create the row of drops
            for raindrop_number in range(int(number_raindrops_x)):
                self._create_raindrop(raindrop_number)
            if (self.raindrop_snow_odd_even == 0):
                self.raindrop_snow_odd_even = 1
            else:
                self.raindrop_snow_odd_even = 0

    def _last_raindrop_row_is_on_screen(self):
        """
        Returns True if all the raindrops are on screen
        """
        for raindrop in self.rainy_weather:
            if (raindrop.y < 0):
                return False
        return True

    def _create_raindrop(self, raindrop_number):
        """Creates a single raindrop"""
        raindrop = RainDrop(self)
        first_spacing = ( self.raindrop_width * self._raindrop_spacing()
            * self.raindrop_snow_odd_even )
        raindrop.x = (first_spacing + raindrop_number * (self.raindrop_width 
            + self.raindrop_width*self._raindrop_spacing()))
        raindrop.y = -raindrop.rect.height
        raindrop.rect.x = raindrop.x
        raindrop.rect.y = raindrop.y
        self.rainy_weather.add(raindrop)

    def _update_rainy_weather(self):
        """
        Creates a row of raindrops if required and allowed and runs the
        update function for raindrop sprites
        """
        if (self.rain):
            self._create_raindrop_row()
        aux_rainy_weather = self.rainy_weather.copy()
        for raindrop in aux_rainy_weather:
            if (raindrop.drop_finished_falling()):
                raindrop.kill()
        self.rainy_weather.update()

    def _create_snowflake_row(self):
        """Creates a row of snowflakes"""
        if (self.snow and self._last_snowflakes_row_is_on_screen()):
            number_snowflakes_x = (self.settings.screen_width 
                // (self.snowflake_width*2))
            # Create the row of snowflakes
            for snowflake_number in range(int(number_snowflakes_x)):
                self._create_snowflake(snowflake_number)
            if (self.raindrop_snow_odd_even == 0):
                self.raindrop_snow_odd_even = 1
            else:
                self.raindrop_snow_odd_even = 0

    def _last_snowflakes_row_is_on_screen(self):
        """
        Returns True if all the raindrops are on screen
        """
        for snowflake in self.snowy_weather:
            if (snowflake.y < 0):
                return False
        return True

    def _create_snowflake(self, snowflake_number):
        """Creates a single snowflake"""
        snowflake = SnowFlake(self)
        first_spacing = ( self.snowflake_width * self.raindrop_snow_odd_even )
        snowflake.x = (first_spacing + snowflake_number * 2 
            * self.snowflake_width)
        snowflake.y = -snowflake.rect.height
        snowflake.rect.x = snowflake.x
        snowflake.rect.y = snowflake.y
        self.snowy_weather.add(snowflake)

    def _update_snowy_weather(self):
        """
        Creates a row of snowflakes if required and allowed and runs the
        update function for snowflake sprites
        """
        if (self.snow):
            self._create_snowflake_row()
        aux_snowy_weather = self.snowy_weather.copy()
        for snowflake in aux_snowy_weather:
            if (snowflake.snowflake_finished_falling()):
                snowflake.kill()
        self.snowy_weather.update()


if __name__ == '__main__':
    pclock = PyGameClock()
    pclock.run_clock()