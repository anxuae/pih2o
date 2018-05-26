# -*- coding: utf-8 -*-

"""Sensors management.
"""

import random
import threading
from RPi import GPIO
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()


class HumiditySensor(object):

    """
    Base class for sensors.
    """

    stype = None

    def __init__(self, pin, power_pin, power_auto=True):
        self.pin = pin
        self.power_pin = power_pin
        self.power_auto = power_auto
        self._lock = threading.Lock()

        GPIO.setup(self.power_pin, GPIO.OUT)
        if not power_auto:
            GPIO.output(self.power_pin, GPIO.HIGH)

    def get_value(self):
        """Return the sensor value.
        """
        with self._lock:
            if self.power_auto:
                GPIO.output(self.power_pin, GPIO.HIGH)
            value = self._read()
            if self.power_auto:
                GPIO.output(self.power_pin, GPIO.LOW)
        return value

    def _read(self):
        raise NotImplementedError


class DigitalHumiditySensor(HumiditySensor):

    stype = 'digital'

    def _read(self):
        """Return True if the sensor has detected a low humidity level.
        """
        return random.choice([True, False])


class AnalogHumiditySensor(HumiditySensor):

    stype = 'analog'

    def _read(self):
        """Return the humidity level measured by the sensor.
        """
        return random.randint(2, 99)
