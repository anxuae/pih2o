#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pih2o main module.
"""

import sys
import atexit
import threading
import argparse
import logging
import flask
from flask_restful import Api
import pih2o
from pih2o import models
from pih2o.api import ApiConfig, ApiControl, ApiData
from pih2o.utils import LOGGER
from pih2o.config import PiConfigParser


class PiApplication(object):

    """Plant watering application which is running in background
    of the Flask application which serves the RESTful API.
    """

    def __init__(self, config):
        self.config = config

        LOGGER.debug("Initializing flask instance...")
        self.flask_app = flask.Flask(pih2o.__name__)
        self.flask_app.config.from_object('pih2o.config')
        self.flask_app.app_context().push() # Make app available for database

        @self.flask_app.route('/pih2o')
        def say_hello():
            return flask.jsonify( {"name": pih2o.__name__, "version": pih2o.__version__} )

        LOGGER.debug("Initializing the database for measurements...")
        models.db.init_app(self.flask_app)
        models.db.create_all()

        LOGGER.debug("Creating RESTful API...")
        self.api = Api(self.flask_app)
        root = '/pih2o/api/v1.0'
        self.api.add_resource(ApiConfig,
                              root + '/config',
                              root + '/config/<string:section>',
                              root + '/config/<string:section>/<string:key>',
                              endpoint='config', resource_class_args=(config,))
        self.api.add_resource(ApiControl,
                              root + '/control',
                              endpoint='control', resource_class_args=(self,))
        self.api.add_resource(ApiData,
                              root + '/data',
                              endpoint='data', resource_class_args=(models.db,))

        atexit.register(self.quit)

    def is_running(self):
        """Return True if the application is running.
        """
        return True

    def start(self):
        """Start the application main loop.
        """

    def main_loop(self):
        """Run the watering application loop.
        """
        print("Not implemented")

    def quit(self):
        """Quit the watering application.
        """
        print("Not implemented")


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
        return PiApplication(config).flask_app # Return the WSGI application
    else:
        sys.exit(0)


if __name__ == '__main__':
    app = create_app()
    app.run()
