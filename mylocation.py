#!/usr/bin/python

import re
import json
import urllib3

class MyLocation:
    """A class to know the location where I am running"""

    def __init__(self):
        """Creates the object with the location"""
        connection = urllib3.connection_from_url('http://ipinfo.io/')
        response = connection.request('GET','/json')
        data = json.loads(response.data.decode('utf-8'))
        self.ip = data['ip']
        self.city = data['city']
        self.region = data['region']
        self.country = data['country']
        latitude,longitude = data['loc'].split(",")
        self.lat = float(latitude)
        self.long = float(longitude)
        self.org = data['org']
        self.postal = data['postal']
        self.timezone = data['timezone']
        self.readme = data['readme']
