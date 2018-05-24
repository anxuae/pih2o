# -*- coding: utf-8 -*-

"""Pih2o database models.
"""

from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Measurement(db.Model):

    __tablename__ = 'measurement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor = db.Column(db.String)
    humidity = db.Column(db.Float)
    triggered = db.Column(db.Boolean)
    record_time = db.Column(db.DateTime)

    def serialize(self):
        json = {}
        for col in self.__table__.columns:
            value = getattr(self, col.name)
            if isinstance(value, (datetime, date)):
                value = value.replace(microsecond=0).isoformat(' ')
            json[col.key] = value
        return json
