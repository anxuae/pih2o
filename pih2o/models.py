# -*- coding: utf-8 -*-

"""Pih2o database models.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Measurement(db.Model):

    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor = db.Column(db.String)
    humidity =db.Column(db.Float)
    triggered = db.Column(db.Boolean)
    record_time = db.Column(db.DateTime)
