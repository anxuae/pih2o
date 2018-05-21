# -*- coding: utf-8 -*-

"""Pih2o configuration.
"""

import ast
import os
import os.path as osp
import subprocess
from collections import OrderedDict as odict
from pih2o.utils import LOGGER

try:
    from configparser import ConfigParser
except ImportError:
    # Python 2.x fallback
    from ConfigParser import ConfigParser


def safe_eval(value):
    """Safely evaluate a string.
    """
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value

#################### Flask configuration keys ####################

SECRET_KEY = "n\x00'\x8c\x98\x95\xe9VwRXk\xc7r\x15X"
SQLALCHEMY_DATABASE_URI = None
SQLALCHEMY_TRACK_MODIFICATIONS = False

##################################################################


DEFAULT = odict((
    ("GENERAL",
        odict((
            ("autostart", (True, "Start pih2o at Raspberry Pi startup")),
        ))
     ),
))


def generate_default_config(filename):
    """Genrate the default configuration.
    """
    with open(filename, 'w') as fp:
        for section, options in DEFAULT.items():
            fp.write("[{}]\n".format(section))
            for name, value in options.items():
                fp.write("# {}\n{} = {}\n\n".format(value[1], name, value[0]))


class PiConfigParser(ConfigParser):

    """Enhenced configuration file parser.
    """

    editors = ['leafpad', 'vi', 'emacs']

    def __init__(self, filename, clear=False):
        ConfigParser.__init__(self)
        self.filename = osp.abspath(osp.expanduser(filename))

        # Update Flask configuration
        global SQLALCHEMY_DATABASE_URI
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + osp.join(osp.dirname(self.filename), 'pih2o.db')

        if not osp.isfile(self.filename) or clear:
            LOGGER.info("Generate the configuration file in '%s'", self.filename)
            dirname = osp.dirname(self.filename)
            if not osp.isdir(dirname):
                os.makedirs(dirname)
            generate_default_config(self.filename)
            if osp.isfile(SQLALCHEMY_DATABASE_URI):
                os.remove(SQLALCHEMY_DATABASE_URI)

        self.reload()

    def reload(self):
        """Reload current configuration file.
        """
        self.read(self.filename)
        # Handle autostart of the application
        self.enable_autostart(self.getboolean('GENERAL', 'autostart'))

    def enable_autostart(self, enable=True):
        """Auto-start pih2o at the Raspberry Pi startup.
        """
        filename = osp.expanduser('~/.config/autostart/pih2o.desktop')
        dirname = osp.dirname(filename)
        if enable and not osp.isfile(filename):

            if not osp.isdir(dirname):
                os.makedirs(dirname)

            LOGGER.info("Generate the auto-startup file in '%s'", dirname)
            with open(filename, 'w') as fp:
                fp.write("[Desktop Entry]\n")
                fp.write("Name=pih2o\n")
                fp.write("Exec=pih2o\n")
                fp.write("Type=application\n")

        elif not enable and osp.isfile(filename):
            LOGGER.info("Remove the auto-startup file in '%s'", dirname)
            os.remove(filename)

    def editor(self):
        """Open a text editor to edit the configuration file.
        """
        for editor in self.editors:
            try:
                process = subprocess.Popen([editor, self.filename])
                process.communicate()
                self.reload()
                return
            except OSError as e:
                if e.errno != os.errno.ENOENT:
                    # Something else went wrong while trying to run the editor
                    raise
        LOGGER.critical("Can't find installed text editor among %s", self.editors)

    def get(self, section, option, **kwargs):
        """Override the default function of ConfigParser to add a
        default value if section or option is not found.
        """
        if self.has_section(section) and self.has_option(section, option):
            return ConfigParser.get(self, section, option, **kwargs)
        return str(DEFAULT[section][option][0])

    def gettyped(self, section, option):
        """Get a value from config and try to convert it in a native Python
        type (using the :py:mod:`ast` module).
        """
        return safe_eval(self.get(section, option))

    def getpath(self, section, option):
        """Get a path from config, evaluate the absolute path from configuration
        file path.
        """
        path = self.get(section, option)
        path = osp.expanduser(path)
        if not osp.isabs(path):
            path = osp.join(osp.relpath(osp.dirname(self.filename), '.'), path)
        return path

    def getall(self, section=None):
        """Return the configuration ad a dictionary.
        """
        if section:
            values = dict((key, safe_eval(value)) for key, value in self._sections[section].items())
        else:
            values = {}
            for name in self._sections:
                values[name] = self.getall(name)
        return values
