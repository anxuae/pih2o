#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pih2o main module.
"""

import os
import sys
import time
import atexit
import threading
import argparse
import logging
from datetime import datetime
from croniter import croniter
import flask
from flask import got_request_exception
from flask_restful import Api
from RPi import GPIO
import pih2o
from pih2o import models
from pih2o.api import ApiConfig, ApiPump, ApiSensors, ApiMeasurements
from pih2o.utils import LOGGER
from pih2o.config import PiConfigParser, SQLALCHEMY_DATABASE_URI
from pih2o.controls.pump import Pump
from pih2o.controls.sensor import AnalogHumiditySensor, DigitalHumiditySensor


class PiApplication(object):

    """Plant watering application which is running in background
    of the Flask application which serves the RESTful API.
    """

    def __init__(self, config):
        self._thread = None
        self._stop = threading.Event()
        self.config = config

        LOGGER.debug("Initializing flask instance")
        self.flask_app = flask.Flask(pih2o.__name__)
        self.flask_app.config.from_object('pih2o.config')
        got_request_exception.connect(self.log_exception, self.flask_app)

        @self.flask_app.route('/pih2o')
        def say_hello():
            return flask.jsonify({"name": pih2o.__name__,
                                  "version": pih2o.__version__,
                                  "running": self.is_running()})

        LOGGER.debug("Initializing the database for measurements")
        models.db.init_app(self.flask_app)
        with self.flask_app.app_context():
            models.db.create_all()

        LOGGER.debug("Initializing the RESTful API")
        self.api = Api(self.flask_app, catch_all_404s=True)
        root = '/pih2o/api/v1'
        self.api.add_resource(ApiConfig,
                              root + '/config',
                              root + '/config/<string:section>',
                              root + '/config/<string:section>/<string:key>',
                              endpoint='config', resource_class_args=(config,))
        self.api.add_resource(ApiPump,
                              root + '/pump',
                              root + '/pump/<int:duration>',
                              endpoint='pump', resource_class_args=(self,))
        self.api.add_resource(ApiSensors,
                              root + '/sensors',
                              root + '/sensors/<int:pin>',
                              endpoint='sensors', resource_class_args=(self,))
        self.api.add_resource(ApiMeasurements,
                              root + '/measurements',
                              endpoint='measurements', resource_class_args=(models.db,))

        # The HW connection of the controls
        GPIO.setmode(GPIO.BOARD)  # GPIO in physical pins mode
        self.pump = None
        self.sensors = []
        self._pump_timer = None

        self.init_controls()

        atexit.register(self.shutdown_daemon)

    def log_exception(self, sender, exception, **extra):
        """Log an exception"""
        sender.logger.error('Got exception during processing: %s', exception)

    def init_controls(self):
        """Initializing HW contols.
        """
        self.pump = Pump(self.config.getint("PUMP", "pin"))

        read_pins = self.config.gettyped("SENSOR", "analog_pins")
        if read_pins:
            # Use analog sensors
            sensor_class = AnalogHumiditySensor
        else:
            # Use digital sensors
            read_pins = self.config.gettyped("SENSOR", "digital_pins")
            sensor_class = DigitalHumiditySensor

        if not read_pins:
            raise ValueError("Neither analog nor digital sensor defined in the configuration")

        for pin in read_pins:
            self.sensors.append(sensor_class(pin, self.config.gettyped("SENSOR", "power_pin"),
                                             self.config.gettyped('SENSOR', 'analog_range')))

    def is_running(self):
        """Return True if the watering daemon is running.
        """
        if self._thread:
            return self._thread.is_alive()
        return False

    def start_watering(self, duration=None):
        """Start the pump for plant watering.

        :param duration: watering duration in seconds
        :type duration: int
        """
        if not self.pump:
            raise EnvironmentError("The pump is not initialized")
        if not duration:
            duration = self.config.getint("PUMP", "duration")
        self.pump.start()
        self._pump_timer = threading.Timer(duration, self.pump.stop)
        self._pump_timer.daemon = True
        self._pump_timer.start()

    def read_sensors(self, sensor_pin=None):
        """Read values from one or all sensors.

        :param sensor_id: pin of the sensor
        :type sensor_id: int
        """
        if not self.sensors:
            raise EnvironmentError("The sensors are not initialized")

        data = []
        for sensor in self.sensors:
            if sensor_pin is not None and sensor.pin != sensor_pin:
                continue

            if sensor.stype == 'analog':
                humidity = sensor.get_value()
                triggered = humidity <= self.config.getfloat("GENERAL", "humidity_threshold")
            else:
                humidity = 0
                triggered = sensor.get_value()

            measure = models.Measurement(**{'sensor': sensor.pin,
                                            'humidity': humidity,
                                            'triggered': triggered,
                                            'record_time': datetime.now()})

            LOGGER.debug("New measurement: sensor=%s, humidity=%s, triggered=%s",
                         sensor.pin, measure.humidity, measure.triggered)

            data.append(measure)

        if not self.config.getboolean("SENSOR", "always_powered"):
            for sensor in self.sensors:
                sensor.power_off()

        return data

    def start_daemon(self):
        """Start the watering daemon main loop.
        """
        if self.is_running():
            raise EnvironmentError("Watering daemon is already running")
        self._stop.clear()
        self._thread = threading.Thread(target=self.main_loop)
        self._thread.daemon = True
        self._thread.start()
        LOGGER.debug("Watering daemon started")

    def main_loop(self):
        """Watering daemon loop.
        """
        cron_pattern = self.config.get('GENERAL', 'record_interval')
        if not croniter.is_valid(cron_pattern):
            raise ValueError("Invalid cron pattern '{}'".format(cron_pattern))

        cron = croniter(cron_pattern)
        next_record = cron.get_next()

        while not self._stop.is_set():
            if self._stop.wait(next_record - time.time()):
                break  # Stop requested

            # Calculate next wakeup time
            next_record = cron.get_next()

            # Take a new measurement
            triggered_sensors = []
            untriggered_sensors = []
            with self.flask_app.app_context():

                for measure in self.read_sensors():
                    models.db.session.add(measure)
                    if measure.triggered:
                        LOGGER.info("Sensor '%s' is triggered", measure.sensor)
                        triggered_sensors.append(measure)
                    else:
                        untriggered_sensors.append(measure)

                models.db.session.commit()

            # Start the watering if necessary (do nothing if already running)
            if float(len(triggered_sensors)) >= float(len(untriggered_sensors)):
                if self.pump.is_running():
                    LOGGER.warning("Skipping watering because pump is already running")
                else:
                    self.pump.start()
                    self._stop.wait(self.config.getint("PUMP", "duration"))
                    self.pump.stop()

    def shutdown_daemon(self):
        """Quit the watering daemon.
        """
        if self._pump_timer:
            self._pump_timer.cancel()

        if self.is_running():
            self._stop.set()
            self._thread.join()
            LOGGER.debug("Watering daemon stopped")

        # To be sure and avoid floor flooding :)
        self.pump.stop()

        GPIO.cleanup()


def create_app(cfgfile="~/.config/pih2o/pih2o.cfg"):
    """Application factory.
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options]", description=pih2o.__doc__)

    parser.add_argument('--version', action='version', version=pih2o.__version__,
                        help=u"show program's version number and exit")

    parser.add_argument("--config", action='store_true',
                        help=u"edit the current configuration")

    parser.add_argument("--reset", action='store_true',
                        help=u"restore the default configuration")

    parser.add_argument("--log", default=None,
                        help=u"save console output to the given file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", dest='logging', action='store_const', const=logging.DEBUG,
                       help=u"report more information about operations", default=logging.INFO)
    group.add_argument("-q", "--quiet", dest='logging', action='store_const', const=logging.WARNING,
                       help=u"report only errors and warnings", default=logging.INFO)

    options, _args = parser.parse_known_args()

    logging.basicConfig(filename=options.log, filemode='w', format='[ %(levelname)-8s] %(name)-18s: %(message)s', level=options.logging)

    config = PiConfigParser(cfgfile, options.reset)

    if options.config:
        LOGGER.info("Editing the automatic plant watering configuration...")
        config.editor()
        sys.exit(0)
    elif not options.reset:
        LOGGER.info("Starting the automatic plant watering application...")
        app = PiApplication(config)
        app.start_daemon()
        return app.flask_app  # Return the WSGI application
    else:
        sys.exit(0)


if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=False)  # Dont want to start the daemon 2 times
