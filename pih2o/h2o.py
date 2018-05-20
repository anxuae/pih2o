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

    def __init__(self, config, db):
        self.config = config
        self.db = db

        atexit.register(self.quit)

    def server_version(self):
        """Return the application version.
        """
        return pih2o.__version__

    def main_loop(self):
        """Run the watering application loop.
        """
        print("Not implemented")

    def quit(self):
        """Quit the watering application.
        """
        print("Not implemented")


def create_app():
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

    config = PiConfigParser("~/.config/pih2o/pih2o.cfg", options.reset)

    if options.config:
        LOGGER.info("Editing the automatic plant watering configuration...")
        config.editor()
        sys.exit(0)
    elif not options.reset:
        LOGGER.info("Starting the automatic plant watering application...")

        # Create falsk application
        app = flask.Flask(pih2o.__name__)
        app.config.from_object('pih2o.config')

        # Initialize the database
        models.db.init_app(app)
        models.db.create_all(app=app)

        # Create PiH2O application
        pih2o_app = PiApplication(config, models.db)

        # Create the RESTful API
        api = Api(app)
        root = '/pih2o/api/v1.0/'
        api.add_resource(ApiConfig, root + '<string:todo_id>',
                         endpoint='config', resource_class_args=(config,))
        api.add_resource(ApiControl, root + '<string:todo_id>',
                         endpoint='control', resource_class_args=(pih2o_app,))
        api.add_resource(ApiData, root + '<string:todo_id>',
                         endpoint='data', resource_class_args=(models.db,))

        return app
    else:
        sys.exit(0)


if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=False)
