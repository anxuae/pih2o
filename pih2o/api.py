# -*- coding: utf-8 -*-

"""Pih2o RESTful API.
"""

from datetime import datetime
from flask import request
from flask_restful import Resource, fields, marshal
from pih2o import config
from pih2o import models

try:
    unicode
except NameError:
    # Python 3.x fallback
    unicode = str


PYTHON_TYPE_TO_FIELD = {
    str: fields.String,
    unicode: fields.String,
    datetime: fields.DateTime,
    float: fields.Float,
    int: fields.Integer,
    list: fields.List,
    bool: fields.Boolean
}


class ApiConfig(Resource):

    def __init__(self, cfg):
        Resource.__init__(self)
        self.cfg = cfg

        self.fields = {}
        for section, options in config.DEFAULT.items():
            for key, value in options.items():
                self.fields.setdefault(section, {})[key] = PYTHON_TYPE_TO_FIELD[type(value[0])]

    def get(self, section=None, key=None):
        if section and key:
            return self.cfg.gettyped(section, key)
        elif section:
            return self.cfg.getall(section)
        else:
            return self.cfg.getall()

    def put(self, section=None, key=None):
        if section and key:
            values = marshal({key: request.json}, self.fields[section], envelope=section)
        elif section:
            values = marshal(request.json, self.fields[section], envelope=section)
        else:
            values = marshal(request.json, self.fields)

        for section, options in values.items():
            for key, value in options.items():
                if value is not None:
                    self.cfg.set(section, key, str(value))

        return '', 204


class ApiPump(Resource):

    def __init__(self, app):
        Resource.__init__(self)
        self.app = app

    def get(self):
        return "Not implemented"


class ApiData(Resource):

    def __init__(self, db):
        Resource.__init__(self)
        self.db = db

    def get(self):
        # Get query string filters
        querry_filters = {}
        for column in models.Measurement.__table__.columns:
            if request.args.get(column.key):
                querry_filters[column.key] = request.args.get(column.key)

        # Build query
        query = self.db.session.query(models.Measurement)
        for key, value in querry_filters.items():
            query = query.filter(getattr(models.Measurement, key).like("%s" % value))
        return [measure.serialize() for measure in query.all()]
