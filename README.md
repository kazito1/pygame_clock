# pygame_clock
**_pygame_clock_ is a simple clock that features an animated background.**

pygame_clock shows the weather by querying [OpenWeather](https://openweathermap.org/).
It gets the location where it is running via IP by querying [ipinfo.io](https://ipinfo.io/)

It can be used fullscreen (the default) or windowed. You can choose between two
possible modes of display: Show photos according to weather or show an animated
background.

## Configure

The configuration is done via the config/pygame_clock.json file.
The following options are supported:

Option              | Default     | Description
--------------------|-------------|------------
fullscreen          | 1           | Sets the mode between fullscreen (1) or windowed (0)
use_photos          | 0           | Choose between using photos to show the weather (1) or an animated background (0)
screen_width        | 800         | Width of screen when windowed
screen_height       | 480         | Height of screen when windowed
bg_color            |[0,0,0]      | Background color when in photo mode. This is visible only when no photo exists.
clock_font          |quicksand    | Font used for displaying text
time_face_percent   |45           | Percentage of screen used by the time
date_face_percent   |10           | Percentage of screen used by date
weather_face_percent|8            | Percentage of screen used by weather
day_text_color      |[0,0,0]      | Text color using during day
night_text_color    |[255,255,255]| Text color using during night
time_format         | %H:%M:%S    | Time format in [strftime](https://strftime.org/) format
date_format         | %A, %B %d   | Date format in [strftime](https://strftime.org/) format
temperature_units   | celsius     | Temperature units. Can be chosen between _celsius_ and _fahrenheit_
api_key             | xxxxxxxxxxx | OpenWeather API Key
queries_per_minute  | 2           | Times to query the OpenWeather API per minute
day_color           |[135,206,235]| Color of the sky during day when using animated background
night_color         |[12,20,69]   | Color of the sky during night when using animated background
cloud_speed         |0.1          | Cloud speed in pixels/update when using animated background. Adjust the value according to your system.
minimum_percent_of_last_cloud|5   | Minumum percent shown of the last cloud created before creating a new cloud when using animated background
raindrop_speed      | 3           | Raindrop falling speed in pixels/update when using animated background. Adjust the value according to your system.
snowflake_speed     | 1           | Snowflake falling speed in pixels/update when using animated background. Adjust the value according to your system.

## Requirements

Pygame for python3 >= 1.9 and pyowm >= 3.0
## Images

The directory images/ should contain the images that are used by the clock.
The following images are required:

**Animated Background Mode**
Filename       | Recommended size | Description
---------------|------------------|------------
sun.png        | 100x100          | Sun
moon.png       | 100x100          | Moon
cloud_day.png  | 100x60           | Cloud during day
cloud_night.png| 100x60           | Cloud during night
raindrop.png   | 25x50            | Single rain drop
snowflake.png  | 50x50            | Single snowflake

**Photo Mode**
Filename            | Description
--------------------|------------------------
clear_day.png       | Clear sky during day
clear_night.png     | Clear sky during night
clouds_day.png      | Cloudy sky during day
clouds_night.png    | Cloudy sky during night
fog_day.png         | Foggy weather during day
fog_night.png       | Foggy weather during night
haze_day.png        | Hazy weather during day
haze_night.png      | Hazy weather during night
hurricane_day.png   | Hurricane during day
hurricane_night.png | Hurricane during night
mist_day.png        | Misty weather during day
mist_night.png      | Misty weather during night
rain_day.png        | Rainy weather during day
rain_night.png      | Rainy weather during day
snow_day.png        | Snowy weather during day
snow_night.png      | Snowy weather during day
storm_day.png       | Storm during day
storm_night.png     | Storm during night
tornado_day.png     | Tornado during day
tornado_night.png   | Tornado during night

_It is recommended that the size of the images in photo mode matches the resolution of your screen_

## Usage

Before the first use, get a free openweather API key at [OpenWeather](https://openweathermap.org/)

Start the clock by running pygame_clock.py:
```shell
$ ./pygame_clock.py
```
