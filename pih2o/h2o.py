#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pih2o main module.
"""

import argparse
import logging
import pih2o
from pih2o.utils import LOGGER
from pih2o.config import PiConfigParser


class PiApplication(object):

    def __init__(self, config):
        self.config = config

    def main_loop(self):
        """Run the application game loop.
        """
        print("Not implemented")


def main():
    """Application entry point.
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
        LOGGER.info("Editing the automatic flower watering configuration...")
        config.editor()
    elif not options.reset:
        LOGGER.info("Starting the automatic flower watering application...")
        app = PiApplication(config)
        app.main_loop()


if __name__ == '__main__':
    main()
