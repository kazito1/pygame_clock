#!/usr/bin/python

import re
import json
import urllib3
from geopy.geocoders import Nominatim


class MyLocation:
    """A class to know the location where I am running"""

    def __init__(self, pclock):
        """Creates the object with the location"""
        self.settings = pclock.settings
        if (hasattr(self.settings,'latitude') and
            hasattr(self.settings,'longitude')):
            self.load_from_nominatim()
        else:
            self.load_from_ipinfo()

    def load_from_ipinfo(self):
        """Sets the location from ipinfo"""
        connection = urllib3.connection_from_url('http://ipinfo.io/')
        response = connection.request('GET','/json')
        data = json.loads(response.data.decode('utf-8'))
        self.city = data['city']
        self.region = data['region']
        self.country = data['country']
        latitude,longitude = data['loc'].split(",")
        self.lat = float(latitude)
        self.long = float(longitude)
        self.postal = data['postal']

    def load_from_nominatim(self):
        """Sets the location data from Nominatim"""
        geolocator = Nominatim(user_agent="pygame_clock")
        coordinates = f"{self.settings.latitude}, {self.settings.longitude}"
        location = geolocator.reverse(coordinates)
        self.city = location.raw['address']['city']
        self.region = location.raw['address']['state']
        self.country = location.raw['address']['country']
        self.lat = float(self.settings.latitude)
        self.long = float(self.settings.longitude)
        self.postal = location.raw['address']['postcode']