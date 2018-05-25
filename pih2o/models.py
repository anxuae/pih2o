# -*- coding: utf-8 -*-

"""Pih2o database models.
"""

from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

try:
    unicode
except NameError:
    # Python 3.x fallback
    unicode = None


class Measurement(db.Model):

    __tablename__ = 'measurement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor = db.Column(db.Integer)
    humidity = db.Column(db.Float)
    triggered = db.Column(db.Boolean)
    record_time = db.Column(db.DateTime)

    def json(self):
        data = {}
        for col in self.__table__.columns:
            value = getattr(self, col.name)
            if isinstance(value, (datetime, date)):
                value = value.replace(microsecond=0).isoformat(' ')

            key = col.key
            if isinstance(col.key, str) and unicode:
                key = unicode(key)
            if isinstance(value, str) and unicode:
                value = unicode(value)
            data[key] = value
        return data
