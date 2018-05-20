# -*- coding: utf-8 -*-

"""Pih2o RESTful API.
"""

from flask_restful import Resource


class ApiConfig(Resource):

    def __init__(self, config):
        Resource.__init__(self)
        self.config = config

class ApiControl(Resource):

    def __init__(self, app):
        Resource.__init__(self)
        self.app = app

class ApiData(Resource):

    def __init__(self, db):
        Resource.__init__(self)
        self.db = db
