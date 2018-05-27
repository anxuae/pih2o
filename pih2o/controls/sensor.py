# -*- coding: utf-8 -*-

"""Sensors management.
"""

import time
import threading
from RPi import GPIO
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()


class HumiditySensor(object):

    """
    Base class for sensors.
    """

    stype = None
    power_state = {}  # Keep power pins of all sensors to mutualize on/off

    def __init__(self, pin, power_pin=0, analog_range=None):
        self.pin = pin
        self.power_pin = power_pin  # 0 means do not manage the power
        self.analog_range = analog_range or []
        self._lock = threading.Lock()

        if self.power_pin and self.power_state.get(self.power_pin) is None:
            GPIO.setup(self.power_pin, GPIO.OUT)  # Never been setup
            self.power_state[self.power_pin] = False

    def power_on(self):
        """Power on the sensor.
        """
        if self.power_pin and not self.power_state[self.power_pin]:
            GPIO.output(self.power_pin, GPIO.HIGH)
            time.sleep(3)  # Make sure the sensor is powered and ready
            self.power_state[self.power_pin] = True

    def get_value(self):
        """Return the sensor value.
        The sensor is automatically powered on if necessary.
        """
        with self._lock:
            self.power_on()
            return self._read()

    def power_off(self):
        """Power off the sensor.
        """
        if self.power_pin and self.power_state[self.power_pin]:
            GPIO.output(self.power_pin, GPIO.LOW)
            self.power_state[self.power_pin] = False

    def _read(self):
        raise NotImplementedError


class DigitalHumiditySensor(HumiditySensor):

    stype = 'digital'

    def __init__(self, *args, **kwargs):
        HumiditySensor.__init__(self, *args, **kwargs)
        GPIO.setup(self.pin, GPIO.IN)

    def _read(self):
        """Return True if the sensor has detected a low humidity level.
        """
        return GPIO.input(self.pin) == GPIO.HIGH


class AnalogHumiditySensor(HumiditySensor):

    stype = 'analog'

    def _read(self):
        """Return the humidity level (in %) measured by the sensor.
        """
        # Choose gain 1 because the sensor range is +/-4.096V
        value = adc.read_adc(self.pin, gain=1)
        return (value - min(self.analog_range)) * 100. / (max(self.analog_range) - min(self.analog_range))
