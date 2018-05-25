# -*- coding: utf-8 -*-

"""Pih2o pump / electro-valve management.
"""

import threading
from pih2o.utils import LOGGER


class Pump(object):

    def __init__(self, pin):
        self.pin = pin
        self._running = threading.Event()

    def is_running(self):
        """
        Return True if the pump is started.
        """
        return self._running.is_set()

    def start(self):
        """
        Start the pump.
        """
        if self.is_running():
            # Avoid starting several times to prevent concurent access
            raise IOError("Watering is already started")

        LOGGER.info("Starting pump (physical pin %s)", self.pin)
        self._running.set()

    def stop(self):
        """
        Stop the pump.
        """
        LOGGER.info("Stoping pump (physical pin %s)", self.pin)
        self._running.clear()
