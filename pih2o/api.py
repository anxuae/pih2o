# -*- coding: utf-8 -*-

"""Pih2o RESTful API.
"""

from datetime import datetime, timedelta
from sqlalchemy import desc
from flask import request
from flask_restful import Resource, fields, marshal
from pih2o import config
from pih2o.models import Measurement

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
    tuple: fields.List,
    bool: fields.Boolean
}


class ApiConfig(Resource):

    def __init__(self, cfg):
        Resource.__init__(self)
        self.cfg = cfg

        self.fields = {}
        for section, options in config.DEFAULT.items():
            for key, value in options.items():
                if isinstance(value[0], (list, tuple)):
                    self.fields.setdefault(section, {})[key] = PYTHON_TYPE_TO_FIELD[type(value[0])](PYTHON_TYPE_TO_FIELD[type(value[0][0])])
                else:
                    self.fields.setdefault(section, {})[key] = PYTHON_TYPE_TO_FIELD[type(value[0])]

    def get(self, section=None, key=None):
        if section and not self.cfg.has_section(section):
            return {"message": "Invalid section '{}'".format(section)}, 400
        if key and not self.cfg.has_option(section, key):
            return {"message": "Invalid key '{}' in section '{}'".format(key, section)}, 400

        if section and key:
            return self.cfg.gettyped(section, key), 200
        elif section:
            return self.cfg.getall(section), 200
        else:
            return self.cfg.getall(), 200

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

        return {}, 204


class ApiPump(Resource):

    def __init__(self, app):
        Resource.__init__(self)
        self.app = app

    def get(self, duration=None):
        try:
            self.app.start_watering(duration)
        except IOError as ex:
            return {"message": str(ex)}, 503
        return {}, 204


class ApiSensors(Resource):

    def __init__(self, app):
        Resource.__init__(self)
        self.app = app

    def get(self, pin=None):
        if pin is None:
            return [sensor.pin for sensor in self.app.sensors], 200
        else:
            return self.app.read_sensors(pin)[0].json(), 200


class ApiMeasurements(Resource):

    def __init__(self, db):
        Resource.__init__(self)
        self.db = db

    def get(self):
        # Get limit of returned value
        limit = request.args.get('lim')
        if limit:
            try:
                limit = int(limit)
            except ValueError as ex:
                return {"message": str(ex)}, 400
        else:
            limit = 10

        # Get query string filters
        querry_filters = {}
        for column in Measurement.__table__.columns:
            value = request.args.get(column.key)
            if value:
                if column == Measurement.record_time:
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    except ValueError as ex:
                        return {"message": str(ex)}, 400
                querry_filters[column.key] = value

        # Build query
        query = self.db.session.query(Measurement)
        for key, value in querry_filters.items():
            if key == Measurement.record_time.key:
                query = query.filter(
                    getattr(Measurement, key) >= value,
                    getattr(Measurement, key) < value + timedelta(seconds=1))
            else:
                query = query.filter(getattr(Measurement, key).like(value))

        return [measure.json() for measure in query.order_by(desc(Measurement.record_time)).limit(limit).all()], 200
