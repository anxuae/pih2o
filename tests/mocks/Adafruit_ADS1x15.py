# -*- coding: utf-8 -*-

"""
Mocks for tests on other HW than Raspberry Pi.
"""

import random


class ADS1115(object):

    def __init__(self):
        pass

    def read_adc(self, pin, gain=1):
        return random.randrange(0, 900, 1)
