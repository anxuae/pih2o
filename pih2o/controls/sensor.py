# -*- coding: utf-8 -*-

"""Sensors management.
"""

import random


class HumiditySensor(object):

    """
    Base class for sensors.
    """

    stype = None

    def __init__(self, pin):
        self.pin = pin

    def get_value(self):
        raise NotImplementedError


class DigitalHumiditySensor(HumiditySensor):

    stype = 'digital'

    def get_value(self):
        """
        Return True if the sensor has detected a low humidity level.
        """
        return random.choice([True, False])


class AnalogHumiditySensor(HumiditySensor):

    stype = 'analog'

    def get_value(self):
        """
        Return the humidity level measured by the sensor.
        """
        return random.randint(2, 99)
