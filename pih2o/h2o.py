#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pih2o main module.
"""

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
import pih2o
from pih2o import models
from pih2o.api import ApiConfig, ApiPump, ApiMeasurements
from pih2o.utils import LOGGER
from pih2o.config import PiConfigParser


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
        self.api.add_resource(ApiMeasurements,
                              root + '/measurements',
                              endpoint='measurements', resource_class_args=(models.db,))

        atexit.register(self.shutdown_daemon)

    def log_exception(self, sender, exception, **extra):
        """Log an exception"""
        sender.logger.error('Got exception during processing: %s', exception)

    def is_running(self):
        """Return True if the watering daemon is running.
        """
        if self._thread:
            return self._thread.is_alive()
        return False

    def start_watering(self, duration=None):
        """
        Start the pump for plant watering.

        :param duration: watering duration in seconds
        :type duration: int
        """
        if not duration:
            duration = self.config.getint("PUMP", "duration")

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

            # Take a new measurement
            next_record = cron.get_next()

            # Dummy measurements
            import random
            with self.flask_app.app_context():
                for i in range(4):
                    humidity = random.randint(2, 99)
                    measurement = models.Measurement(sensor=hex(i),
                                                     humidity=humidity,
                                                     triggered=humidity < 30,
                                                     record_time=datetime.now())
                    LOGGER.debug("Add new measurement for sensor '%s'", i)
                    models.db.session.add(measurement)
                models.db.session.commit()

    def shutdown_daemon(self):
        """Quit the watering daemon.
        """
        if self.is_running():
            self._stop.set()
            self._thread.join()
            LOGGER.debug("Watering daemon stopped")


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
    app.run()
